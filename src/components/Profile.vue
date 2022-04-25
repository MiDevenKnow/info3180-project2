<template>
 <body style="margin-top:0px; padding-bottom:10rem; margin-top:-40px;">
        <div class="d-flex align-items-center justify-content-center" style="margin-top:-240px;" >
            <div>
                <div class="card mb-3 pb-2" style="width: 900px; margin-top:270px;">
                    <div class="row no-gutters">
                        <div class="col-md-3 p-2 pt-4 pl-4 mr-3">
                            <img v-bind:src="user.photo" class="card-img-top" style="border-radius:50%; width:200px;height:200px;" alt="User Images"/>
                        </div>
                        <div class="col-md-4">
                            <div class="card-body">
                                <h2 class="card-title font-weight-bold">{{user.name}}</h2>
                                <p class="card-text font-weight-bold" style="color:#95989e; font-size:25px; margin-top:-10px;">@{{user.username}}</p>
                                <p class="card-text" style="color:#95989e;">{{user.biography}}</p>
                            
                                <div class="row">
                                    <span class="d-flex col">
                                        <p class="mr-5" style="color:#95989e;">Email </p>
                                        <p class="font-weight-bold">{{user.email}}</p>
                                    </span>
                                    <span class="d-flex col">
                                        <p class="mr-4" style="color:#95989e;">Location</p>
                                        <p class="font-weight-bold">{{user.location}}</p>
                                    </span>
                                    <span class="d-flex col">
                                        <p class="pr-3 mr-4" style="color:#95989e;">Joined</p>
                                        <p class="font-weight-bold">{{user.date_joined}}</p>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <h2 class="font-weight-bold d-flex align-items-center  justify-content-center" style="margin-right:720px;">Cars Favourited</h2>
        <div class="card-layout d-flex align-items-center  justify-content-center" style="margin-left:40px; margin-top:0px;">
        <div id='carddd'>
        <div v-for="cars in cars" :key="cars" class="card mb-4 mr-4" style="width: 19rem;  border-radius:10px;">
        <div class="h-100 w-100">
            <img v-bind:src="cars.photo" class="card-img-top" style="height: 15rem;" alt="Car Images"/>
        </div>
        <div class="card-body" style="height:12rem;">
            <div class="row">
                <h6 class="font-weight-bold card-title col">{{cars.year}} {{cars.make}}</h6> 
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
            <button style="height:40px; border-radius:10px;" @click="$router.push({ name: 'carDetails', params: { car_id: cars.id } })" class="btn btn-success w-100">View more details</button>                
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
            user:[],
            success:[],
            cars:[]
           
        }
    },
    created: function(){
            this.getCsrfToken();
            let router =this.$router;
            let user_id = JSON.parse(localStorage.getItem('id'));
            let self=this;

        
            fetch("/api/users/"+user_id+"/favourites", {
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
                    console.log("error")
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
    },
    mounted: function(){
        let router =this.$router;
        let user_id =localStorage.getItem('id') ;
        let self=this;
        fetch("/api/users/"+user_id, {
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
                console.log('error')
            }
            
            return response.json();

        })
        .then(function (jsonResponse) {
            if ('data' in jsonResponse ){
                // self.success =  jsonResponse.message.message;
                // self.message = 'success';
                self.user=jsonResponse.data
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
    },
    methods: {
        getCsrfToken() {
            let self = this;
            fetch('/api/csrf-token')

            .then((response) => response.json())

            .then((data) => {
                console.log(data);
                self.csrf_token = data.csrf_token;
            })
        }
    }
}
</script>