<template>
  <body style="padding-top: 5rem; padding-bottom:10rem; margin: 0; " >
        <div class="d-flex align-items-center justify-content-center h-100" style="margin-top:-20px;" >
            <div class="">
            <h2 class="font-weight-bold" style="font-size:40px;">Explore</h2>
            <br>
                <div id = "message">
                    <p class="alert alert-success" v-if="message === 'success'" >Car/s Found!</p>
                    <ul class="alert alert-danger" v-if="message === 'error'" >
                        <li v-for="errors in errors" :key="errors"> {{errors}}</li>
                    </ul> 
                </div>
                <div class="card p-3  mb-4" style="width: 65rem; border-radius:10px;">
                    <div class="card-body">
                    <div class="form-row ">
                    <div class="form-group col">
                        <label  class="font-weight-bold" for="make">Make</label>
                        <input name="make" v-model="makeSearch" id="make" type="text" class="form-control " style="height:50px; width:350px; margin-right:20px; border-radius:10px;">
                    </div>
                    <div class="form-group col">
                        <label class="font-weight-bold" for="model">Model</label>
                        <input name="model" type="text" v-model="modelSearch" class="form-control" style="height:50px; width:350px; margin-right:20px; border-radius:10px;">
                    </div>
                    <div class="form-group col " style="margin-top:30px;">
                    <button type="submit"  @click="search"  style="height:50px; border-radius:10px;" class="btn btn-success w-100">Search</button>
                    </div>
                </div>
                    <br>
                    </div>
                </div>
            </div>
         </div>
         <div class="card-layout d-flex align-items-center  justify-content-center" style="margin-left:40px; margin-top:50px;">
            <div id='carddd'>
            <div v-for="cars in cars" :key="cars" class="card mb-4 mr-4" style="width: 22rem;  border-radius:10px;">
            <div class="h-100 w-100">
                <img v-bind:src="cars.photo" class="card-img-top" style="height: 15rem;" alt="Car Images"/>
            </div>
            <div class="card-body" style="height:12rem;">
                <div class="row">
                    <h5 class="font-weight-bold card-title col">{{cars.year}} {{cars.make}}</h5> 
                    <div >
                        <span class="d-flex p-1 btn-success align-items-center justify-content-center" style="float:right;border-radius:10px; height:35px;" >
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-tag mr-1" viewBox="0 0 16 16">
                            <path d="M6 4.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm-1 0a.5.5 0 1 0-1 0 .5.5 0 0 0 1 0z"/>
                            <path d="M2 1h4.586a1 1 0 0 1 .707.293l7 7a1 1 0 0 1 0 1.414l-4.586 4.586a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 1 6.586V2a1 1 0 0 1 1-1zm0 5.586 7 7L13.586 9l-7-7H2v4.586z"/>
                            </svg> 
                            <span> {{"$"+Number(cars.price).toLocaleString() }}</span>
                        </span>
                    </div>
                </div>

                <p class="card-text" style="margin-top:-10px;color:#95989e;">{{cars.model}}</p><br><br>
                <button style="height:40px; border-radius:10px;" @click="$router.push({ name: 'carDetails', params: { car_id: cars.id } })" class="btn btn-success w-100 mb-2">View more details</button>                
            </div>
        </div>
            
            </div>

        </div>    
    </body>
</template>

<script>
export default {
   data() {
        return {
            csrf_token: '',
            message: '',
            errors: [],
            success:[],
            cars:[],
            makeSearch:'',
            modelSearch:''
          
        }
    },
    methods: {
        search: function(){
            let router =this.$router;
            let self=this;
            fetch('/api/search?make='+self.makeSearch+'&'+'model='+self.modelSearch, {
                method: "GET",
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    Authorization: 'Bearer ' + localStorage.getItem('token')
    
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                if(response.status==401){
                    //router.push('/error')
                    console.log('error');
                }
                return response.json();
            })
            .then(function (jsonResponse) {
                if ('data' in jsonResponse ){
                    // self.success =  jsonResponse.message.message;
                    self.message = 'success';
                
                    self.cars=jsonResponse.data
                    console.log(jsonResponse)
                } else if ('errors' in jsonResponse ){
                    console.log(jsonResponse)
                    self.cars=[]
                    self.errors = jsonResponse.errors.errors;
                    self.message = 'error';
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        getCsrfToken() {
            let self = this;
            fetch('/api/csrf-token')

            .then((response) => response.json())

            .then((data) => {
                console.log(data);
                self.csrf_token = data.csrf_token;
            })
        }
    },
    created() {
        this.getCsrfToken();
    },
    mounted: function(){
        let router =this.$router;
        let self=this;
        fetch("/api/cars", {
            method: "GET",
            headers: {
                'X-CSRFToken': this.csrf_token,
                Authorization: 'Bearer ' + localStorage.getItem('token')

            },
            credentials: 'same-origin'
        })
        .then(function (response) {
            if(response.status==401){
                console.log('error');
            }
            return response.json();
        })
        .then(function (jsonResponse) {
            if ('data' in jsonResponse ){
                // self.success =  jsonResponse.message.message;
                // self.message = 'success';
                self.cars=jsonResponse.data
                console.log(jsonResponse)
            } else if ('errors' in jsonResponse ){
                console.log(jsonResponse)
                // self.errors = jsonResponse.errors.errors;
                // self.message = 'error';
            }
        })
        .catch(function (error) {
            console.log(error);
        });
    }
}
</script>