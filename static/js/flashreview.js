function showans(x) {
    var T = document.getElementById("answer"+x);
    T.style.display = "block";  // <-- Set it to block
    var B = document.getElementById("ansbutton"+x);
B.style.display = "none";
}
const store = new Vuex.Store({
    state: {
      muserid: null,
      mdeckid:null,
    },
    mutations: {
      create_muserid(state, value){
          state.muserid = value;
      },
      create_mdeckid(state, value){
          state.mdeckid=value;
      }
    },
    getters: {
      get_muserid: function(state) {
          return state.muserid;
      },
      get_mdeckid: function(state){
          return state.mdeckid;
      }
    }
    
  })

  const cardrev = Vue.component('cardrev', {
    template: `
    <div class="container d-flex align-items-center justify-content-center">    
    <br>
        <div v-if="check_empty">
            <div class="card align-middle" style="width: 50rem">
            <div class="card-body align-middle">
            <h5 class="card-header">{{curr_card['front']}}</h5>
            <div v-if="show_">
                <p class="card-text">{{curr_card['back']}}</p>
                <div class="card-footer align-bottom">
                    <div class="btn-group btn-group-toggle" data-toggle="buttons">
                    <label class="btn btn-success">
                    <input type="radio" name="options" id="option1" autocomplete="off" v-model="diff" value="1"> Easy
                    </label>
                    <label class="btn btn-warning">
                    <input type="radio" name="options" id="option2" autocomplete="off" v-model="diff" value="2"> Medium
                    </label>
                    <label class="btn btn-danger">
                    <input type="radio" name="options" id="option3" autocomplete="off" v-model="diff" value="3"> Hard
                    </label>
                    <button class="btn btn-primary" @click="next()">Next</button>
                </div>
                </div>
            </div>
            <div v-else>
                <button class="btn btn-primary" @click="show()">Show Answer</button>
            </div>
            </div>
            </div>
        </div>
        <div v-else> <h3>No Cards on this Deck. Add Cards to review</h3></div>
    </div>
    </div>`,
        data: function() {
            return {
                cards: [],
                card_ids:[],
                front: '',
                back: '',
                show_: false,
                deid:store.getters.get_mdeckid,
                current: 0,
                curr_id:null,
                diff:null,
            }
        },methods: {
            get_cards: function(){
                link="/api/"+this.user_id+'/'+this.deck_id;
                fetch(link, {
                headers: {
                'Accept': 'application/json',
                //'Authentication-Token': getCookie("actok"),
                }
            }).then(r => r.json())
            .then(d => JSON.parse(d))
            .then(deks => this.cards=deks)
            .catch((error) => {
                console.error('Error:', error);});
            },
            show: function(){
                this.show_=true;
            },
            next: function(){
                if (this.current<this.card_len-1){
                    this.current+=1;
                    //console.log(this.diff);
                    this.show_=false;
                    link="/api/"+this.user_id+'/'+this.deck_id+'/'+this.card_ids[this.current];
                    fetch(link, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                "diff": this.diff
                            }),
                        })
                        .then(response => {
                            console.log(response, "Updated");
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                        });
                
                } else {
                    link="/api/"+this.user_id+'/'+this.deck_id+'/'+this.card_ids[this.current];
                    fetch(link, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                "diff": this.diff
                            }),
                        })
                        .then(response => {
                            console.log(response, "Updated");
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                        });
                    alert("Finished Reviewing")
                    window.location = "/dashboard/"+this.user_id+"/#/deck_list";
                }
                
            }
            
        },
        computed: {
            user_id(){
                return store.state.muserid;
            },
            deck_id(){
                return store.getters.get_mdeckid;
            },
            check_empty: function(){
                if (this.card_len>0){
                    //console.log("Not empty")
                    return true
                } else {
                    return false
                }
            },
            cards_(){
                return this.cards;
            },
            card_len: function(){
                let count=0
                for (v in this.cards){
                    count+=1;
                    this.card_ids.push(v)
                }
                //console.log(this.cards)
                //console.log(this.card_ids.length, count)
                return count;
            },
            curr_card: function(){
                //console.log(this.card_ids[this.current])
                return this.cards[this.card_ids[this.current]]
            }
        },
        mounted: async function() {
            await new Promise(r => setTimeout(r, 10));
            this.deid=store.getters.get_mdeckid;
            link="/api/"+this.user_id+"/"+this.deid+'';
            console.log(this.deid+' '+link);
            fetch(link, {
                headers: {
                  'Accept': 'application/json',
                  //'Authentication-Token': getCookie("actok"),
                }
              }).then(r => r.json())
              .then(d => JSON.parse(d))
              .then(deks => {this.cards=deks;})
              .catch((error) => {
                console.error('Error:', error);
            })
        },
        created: async function(){
            this.deid=store.getters.get_mdeckid;
            console.log(this.deid)
        }     
        }
)

var app = new Vue({
    el: '#app',
    store: store,
    data: {
        grand_total: 0,
        show_log: false,
        userid:null,
        deckid:null,
    },
    created: function () {
        // `this` points to the vm instance
        this.userid=window.location.href.split('/')[3];
        store.commit('create_muserid', this.userid);
        this.deckid=window.location.href.split('/')[4];
        store.commit('create_mdeckid', this.deckid);
        //console.log(this.userid +' '+ this.deckid)
        console.log("Let there be light")
      },
    methods: {
        add_grand_total: function() {
            console.log("in grand_total");
            this.grand_total = this.grand_total + 1;
        },
    }

})