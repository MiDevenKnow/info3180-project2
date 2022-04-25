<template>
    <body style="height: 100vh; margin-top:-30px;">
    <div class="d-flex align-items-center justify-content-center h-100" style="flex-direction: column; margin-top:-30px;">
            <div id = "message" style="width:1000px;" >
            <p class="alert alert-success" v-if="message === 'success'" >{{success}}</p>
            <ul class="alert alert-danger" v-if="message === 'error'" >
                <li v-for="errors in errors" :key="errors"> {{errors}}</li>
            </ul> 
            </div>
        <div style="width: 1700px;">
            <div class="" style="margin-top:0px;" >
                <div class="row g-0 no-gutters justify-content-center ">
                <div class="col-md-3  rounded" >
                    <img v-bind:src="cars.photo" class="card-img-top h-100" alt="Car Images"/>
                </div>
                <div class="col-md-4 pr-3 bg-white  rounded" >
                    <div class="card-body ">

                    <div class="card-body">
                    <h2 class="card-title font-weight-bold">{{cars.year}} {{cars.make}}</h2>
                    <p class="card-text font-weight-bold" style="color:#95989e; font-size:25px; margin-top:-10px;">{{cars.model}}</p>
                    <p class="card-text" style="color:#95989e;">{{cars.description}}</p>
                </div>
                <div class="row">
                    <span class="d-flex col">
                        <p class="mr-5 ml-3" style="color:#95989e;">Color </p>
                        <p class="font-weight-bold">{{cars.colour}}</p>
                    </span>
                    <span class="d-flex col">
                        <p class="mr-5" style="color:#95989e;">Body Type </p>
                        <p class="font-weight-bold">{{cars.car_type}}</p>
                    </span>
                </div>

                <div class="row">
                    <span class="d-flex col">
                        <p class="mr-5 ml-3 " style="color:#95989e;">Price </p>
                        <p class="font-weight-bold">{{"$"+Number(cars.price).toLocaleString() }}</p>
                    </span>
                    <span class="d-flex col">
                        <p class="mr-4" style="color:#95989e;">Transmission</p>
                        <p class="font-weight-bold">{{cars.transmission}}</p>
                    </span>
                </div>
                <br><br><br><br><br><br>
                <div class="row">
                <span class="d-flex col">
                    <button class="btn btn-success mt-4" style="height:40px;" type="submit">Email Owner</button>
                </span>
                <span class="d-flex col">
                    <input id="toggle-heart" class="mr-5 mt-4" v-on:click="favorites(cars.id)"  type="checkbox" /> 
                    <label style="margin-left:300px; " class="mt-4" for="toggle-heart">❤</label>
                </span>
                </div>
        </div>
      </div>
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
            cars:[],
            success:[]
           
        }
    },
    mounted: function(){
        let router =this.$router;
        let car_id = this.$route.params.car_id;
        let self=this;

        fetch("/api/cars/"+car_id, {
            method: "GET",
            headers: {
                'X-CSRFToken': this.csrf_token,
                Authorization: 'Bearer ' + localStorage.getItem('token')
            },
            credentials: 'same-origin'
        })
        .then(function (response) {
            if(response.status==401){
                router.push('/error')
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
    methods:{
        favorites(car_id){
            let router =this.$router;
            let self=this;
            fetch("/api/cars/"+car_id+"/favourite", {
                method: "POST",
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                if(response.status==401){
                    router.push('/error')
                }
                return response.json();
            })
            .then(function (jsonResponse) {
                if ('data' in jsonResponse ){
                    self.success =  jsonResponse.data.message;
                    self.message = 'success';
                    console.log(jsonResponse)
                } else if ('errors' in jsonResponse ){
                    console.log(jsonResponse)
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
}
</script>