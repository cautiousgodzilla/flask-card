function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
const store = new Vuex.Store({
    state: {
      muserid: null,
      deckid:null,
    },
    mutations: {
      create_muserid(state, value){
          state.muserid = value;
      },
      change_deckid(state, value){
          console.log("changed")
          state.deckid=value;
      }
    },
    getters: {
      get_muserid: function(state) {
          return state.muserid;
      },
      get_deckid: function(state){
          return state.deckid;
      }
    }
    
  })
const deck_list = Vue.component('deck_list', {
    template: `
    <div class="text-center">    
    <div class="form-group">
    <br>
    <button v-if="!show_add" @click="show_add = !show_add" class="btn btn-primary">Add New Deck</button>
    
    <form v-if="show_add" action="" method="">
        <input  type="text" placeholder="Topic" name="topic" v-model="topic">
        <button class="btn btn-primary" v-on:click="addDeck(); get_deck()">Add</button>
    </form>
    
    </div>
    <br>
    <table id = "all-decks" class="table table-bordered">
        <thead class="table-dark">
        <tr >
        <th scope="col">Deck ID</th>
        <th scope="col">Deck name</th>
        <th scope="col">Last Review</th>
        <th scope="col">Actions</th>            
        </tr>
        </thead>
        <tbody>
        <tr scope="row" v-for="(valu, decky) in decks_">
            <td> {{decky}}</td>
            <td> {{valu["topic"]}}</td>
            <td> {{valu["last_review"]}}</td>
            <td> 
                
                <a  class="btn btn-primary btn active" :href="'/'+user_id+'/'+decky+'/review2'" >Review </a>
                <button tag="button" class="btn btn-outline-primary" v-on:click='send_did(decky)'><router-link to="/card_list">Edit Deck</router-link></button>
                <a  role="button" class="btn btn-outline-primary" @click='send_did(decky);delete_deck();' >Delete</a>
                
            </td>
        </tr>
        </tbody>
            <br>
        </table>
        </div>`,
        data: function() {
            return {
                decks: [],
                topic: '',
                show_add: false,
                did: null,
            }
        },methods: {
            send_did: function(variable){
                    //this.did=document.getElementById("did").value;
                    this.did=variable;
                    store.commit('change_deckid', this.did);
                    console.log(store.getters.get_deckid);
            },
            delete_deck: function(){
                link='/api/'+this.user_id+'/'+this.did;
                fetch(link, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => {alert("Deck Deleted");})
                .catch((error) => {
                    console.error('Error:', error);
                });
                this.get_deck();
                console.log("Updated deck")
            },
            get_deck: function(){
                link="/api/"+this.user_id;
                fetch(link, {
                headers: {
                  'Accept': 'application/json',
                  'Authentication-Token': getCookie("actok"),
                }
              }).then(r => r.json())
              .then(d => JSON.parse(d))
              .then(deks => this.decks=deks)
              .catch((error) => {
                console.error('Error:', error);});

            },
            addDeck: function() {
                link='/api/'+this.user_id;
                fetch(link, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            "topic": this.topic
                        }),
                    })
                    .then(response => {alert("Deck Created");this.show_add=false})
                    .catch((error) => {
                        console.error('Error:', error);;
                    });
            }
        },
        computed: {
            user_id(){
                return store.state.muserid;
            },
            decks_(){
                return this.decks;
            }
        },
        mounted: async function() {
            link="/api/"+this.user_id;
            r = await fetch(link, {
                headers: {
                  'Accept': 'application/json',
                  'Authentication-Token': getCookie("actok"),
                }
              });
            d = await r.json(); 
            const deks = JSON.parse(d);   
            this.decks=deks;
            }
        }
)
const card_list = Vue.component('card_list', {
    template: `
    <div class="text-center">    
    <div class="form-group">
    <br>
    <button v-if="!show_add" @click="show_add = !show_add" class="btn btn-primary">Add New card</button>
    
    <div v-if="show_add" action="#card_list" method="">
        <input  type="text" placeholder="Front" name="front" v-model="front">
        <input  type="text" placeholder="Back" name="back" v-model="back">
        <button class="btn btn-primary" v-on:click="addCard();get_cards()">Add</button>
    </div>
    <br>
    <div>
    <button class="btn btn-outline-primary"><router-link to="/deck_list" >Go Back</router-link></button>
    </div>
    
    </div>
    <br>
    <table id = "all-cards" class="table table-bordered" v-if="check_empty">
        <thead class="table-dark">
        <tr >
        <th scope="col">Card ID</th>
        <th scope="col">Front</th>
        <th scope="col">Back</th>
        <th scope="col">Next Review</th>
        <th scope="col">Interval</th>
        <th scope="col">Actions</th>            
        </tr>
        </thead>
        <tbody>
        <tr scope="row" v-for="(valu, cardy) in cards_">
            <td> {{cardy}}</td>
            <td> {{valu["front"]}}</td>
            <td> {{valu["back"]}}</td>
            <td> {{valu["time"]}}</td>
            <td> {{valu["interval"]}}</td>
            <td> 
                <a  class="btn btn-primary btn active" :href="'/'+user_id+'/'+deck_id+'/'+cardy+'/update'" >Edit Card</a>
                <a  role="button" class="btn btn-outline-primary" @click='send_cid(cardy);delete_card();' >Delete</a>
            </td>
        </tr>
        </tbody>
            <br>
        </table>
        <h3 v-else> No Cards on this Deck. Click on Add Cards</h3>
        </div>`,
        data: function() {
            return {
                cards: [],
                front: '',
                back: '',
                show_add: false,
                deid:store.getters.get_deckid,
                empty: false,
                cid: null,
            }
        },methods: {
            send_cid: function(variable){
                //this.did=document.getElementById("did").value;
                this.cid=variable;
                console.log(this.cid);
            },
            delete_card: function(){
                link='/api/'+this.user_id+'/'+this.deck_id+'/'+this.cid;
                fetch(link, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => {alert("Card Deleted");})
                .catch((error) => {
                    console.error('Error:', error);
                });
                this.get_cards();
                console.log("Updated card list")
            },addCard: function() {
                link='/api/'+this.user_id+'/'+this.deck_id;
                fetch(link, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            "front": this.front,
                            "back": this.back
                        }),
                    })
                    .then(response => {
                        console.log(response);
                        alert("Card Created");
                        this.show_add=false;
                        this.empty=true;

                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                    this.get_cards();
                    this.front='';this.back='';
                    console.log("got cards")
            },
            get_cards: function(){
                link="/api/"+this.user_id+'/'+this.deck_id;
                fetch(link, {
                headers: {
                'Accept': 'application/json',
                'Authentication-Token': getCookie("actok"),
                }
            }).then(r => r.json())
            .then(d => JSON.parse(d))
            .then(deks => this.cards=deks)
            .catch((error) => {
                console.error('Error:', error);});
            },
            
        },
        computed: {
            user_id(){
                return store.state.muserid;
            },
            deck_id(){
                return store.getters.get_deckid;
            },
            check_empty: function(){
                if (this.empty===true){
                    return true
                } else {
                    return false
                }
            },
            cards_(){
                return this.cards;
            }
        },
        mounted: async function() {
            await new Promise(r => setTimeout(r, 10));
            this.deid=store.getters.get_deckid;
            link="/api/"+this.user_id+"/"+this.deid+'';
            console.log(this.deid+' '+link);
            fetch(link, {
                headers: {
                  'Accept': 'application/json',
                  'Authentication-Token': getCookie("actok"),
                }
              }).then(r => r.json())
              .then(d => JSON.parse(d))
              .then(deks => {this.cards=deks;this.empty=true;})
              .catch((error) => {
                console.error('Error:', error);
            })
        },
        created: async function(){
            this.deid=store.getters.get_deckid;
            console.log(this.deid)
        }
            ///change this to computed or something else so that it adds new deck
            ///Note 2 not needed I guess
            
        }
)
const home = Vue.component('home', {
    template: `
    <div>
      <h3> User Details </h3>
        <div><button class="btn btn-outline-primary"><a href="/logout">Logout</a></button></div>
        <p>Current User: {{ user_id }}</p>
        <p>API Key: {{token }}</p>
    </div>`,
    computed: {
        user_id(){
            return store.state.muserid;
        },
        token(){
            return getCookie("actok")
        }
    }
})

const MessageBoard = Vue.component('message-board', {
    template: `
    <div>
          <div class="form-group">
            <form action="" method="">
                <input type="text" placeholder="Email" name="email" value="Your Email" v-model="vname">
                <input type="password" placeholder="Password" name="password" value="" v-model="vpass">
            </form>
            <button class="btn btn-primary" v-on:click="sayHi">Login</button>
          </div>
    </div>
        `,
    data: function() {
        return {
            vname: null,
            vpass: null,
            vmuserid:store.getters.get_muserid,
        }
    },
    methods: {
        sayHi: function() {
            fetch('/login?include_auth_token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "email": this.vname,
                        "password": this.vpass
                    }),
                })
                .then(response => response.json())
                .then(da => da["response"]["user"]["authentication_token"])
                .then(tok => {
                    document.cookie = "actok="+tok+"; path=/;";
                    console.log(document.cookie);
            })
                .then(response => {
                if(true){
                    window.location.href = '/'
                }
                else{
                    alert(response.message)
                }
            })
                .catch((error) => {
                    console.error('Error:', error);;
                });
        }
    },
    computed: {

        },
})

const NotFound = Vue.component('not_found', { template: '<p>Page not found</p>' })

const routes = [{
    path: '/login',
    component: MessageBoard
},{
    path: '/deck_list',
    component: deck_list
}, {
    path: '/card_list',
    component: card_list
}, {
    path: '/',
    component: home
},{
    path: '*',
    component: NotFound
}];

const router = new VueRouter({
  routes // short for `routes: routes`
})


var app = new Vue({
    el: '#app',
    router: router,
    store: store,
    data: {
        grand_total: 0,
        show_log: false,
        userid:null,
    },
    created: function () {
        // `this` points to the vm instance
        this.userid=document.getElementById("uid").defaultValue;
        store.commit('create_muserid', this.userid);
        console.log("Let there be light")
      },
    methods: {
        add_grand_total: function() {
            console.log("in grand_total");
            this.grand_total = this.grand_total + 1;
        },
    }

})