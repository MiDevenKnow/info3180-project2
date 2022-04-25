<template>
   <body style="margin-top: -20px">
        <div class="d-flex align-items-center justify-content-center h-100" style="" >
            <div class="">
                <h2 class="font-weight-bold " >Add New Car</h2>
                <br>
                <form @submit.prevent="registerCar" id="carForm">
                <div id = "message">
                    <p class="alert alert-success" v-if="message === 'success'" >Car Successfully Added!</p>
                    <ul class="alert alert-danger" v-if="message === 'error'" >
                        <li v-for="errors in errors" :key="errors"> {{errors}}</li>
                    </ul> 
                </div>
                    <div class="card p-4 mb-5" style="width: 55rem; border-radius:10px;">
                        <div class="card-body">
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="make">Make</label>
                                    <input name="make" type="text" class="form-control " style="height:50px; width:370px; border-radius:10px;">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="font-weight-bold" for="model">Model</label>
                                    <input name="model" type="text" class="form-control" style="height:50px; width:370px; border-radius:10px;">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="colour">Colour</label>
                                    <input name="colour" type="text" class="form-control" style="height:50px; width:370px; border-radius:10px;">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="font-weight-bold" for="year">Year</label>
                                    <input name="year" type="text" class="form-control" style="height:50px;  width:370px; border-radius:10px;">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="price">Price</label>
                                    <input name="price" type="number" class="form-control" style="height:50px; width:370px; border-radius:10px;">
                                </div>
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="ctype">Car Type</label>
                                    <select name="ctype" class="custom-select" style="height:50px; width:370px; border-radius:10px;">
                                        <option value="SUV">SUV</option>
                                        <option value="MPV">MPV</option>
                                        <option value="Micro">Micro</option>
                                        <option value="Hatchback">Hatchback</option>
                                        <option value="Sedan">Sedan</option>
                                        <option value="Wagon">Wagon</option>
                                        <option value="Luxury">Luxury</option>
                                        <option value="Antique">Antique</option>
                                        <option value="Muscle">Muscle</option>
                                        <option value="Electric">Electric </option>
                                        <option value="Supercar"> Supercar</option>
                                        <option value="Convertible">Convertible</option>
                                        <option value="Coupe">Coupe</option>
                                    </select>                                
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="transmission">Transmission</label>
                                    <select name="transmission" class="custom-select" style="height:50px; width:370px; border-radius:10px;">
                                        <option value="Automatic">Automatic</option>
                                        <option value="Manual">Manual</option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group w-100">
                                    <label  class="font-weight-bold" for="description">Description</label>
                                    <textarea name="description" class="form-control w-100 " style="height:150px; border-radius:10px;"></textarea>
                                </div>
                            </div>
                            <div class="form-group">
                                <label  class="font-weight-bold" for="photo">Upload Photo</label>
                                <input name="photo" class="form-control-file" type="file">
                            </div><br>
                            <button type="submit" style="height:45px; width:200px; border-radius:10px;" class="btn btn-success">Save</button>
                        </div>
                    </div>
                </form>
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
            success:[]
        }
    },
    methods: {
        registerCar: function(){
            let carForm= document.getElementById('carForm');
            let router =this.$router;
            let form_data=new FormData(carForm);
            let self=this;
            fetch("/api/cars", {
                method: "POST",
                body: form_data,
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
                if ('message' in jsonResponse ){
                    self.success =  jsonResponse.message.message;
                    self.message = 'success';
                    setTimeout(() => {
                        router.push('/explore')
                    }, 1500); 

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