<template>
  <body style="">
        <div class="d-flex align-items-center justify-content-center h-100" style="margin-top:-40px;" >
            <div class="">
                <h2 class="font-weight-bold " >Register New User</h2>
                <br>
                <form @submit.prevent="registerUser" id="registerForm">
                <div id = "message">
                    <p class="alert alert-success" v-if="message === 'success'" >{{success}}</p>
                    <ul class="alert alert-danger" v-if="message === 'error'" >
                        <li v-for="errors in errors" :key="errors"> {{errors}}</li>
                    </ul> 
                </div>
                    <div class="card p-4 mb-5" style="width: 55rem; border-radius:10px;">
                        <div class="card-body">
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="username">Username</label>
                                    <input name="username" type="text" class="form-control " style="height:50px; width:370px; border-radius:10px;">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="font-weight-bold" for="password">Password</label>
                                    <input name="password" type="password" autocomplete="on" class="form-control" style="height:50px; width:370px; border-radius:10px;">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="name">Fullname</label>
                                    <input name="name" type="text" class="form-control" style="height:50px; width:370px; border-radius:10px;">
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="font-weight-bold" for="email">Email</label>
                                    <input name="email" type="email" class="form-control" style="height:50px;  width:370px; border-radius:10px;">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label  class="font-weight-bold" for="location">Location</label>
                                    <input name="location" type="text" class="form-control" style="height:50px; width:370px; border-radius:10px;">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group w-100">
                                    <label  class="font-weight-bold" for="biography">Biography</label>
                                    <textarea name="biography" class="form-control w-100 " style="height:150px; border-radius:10px;"></textarea>
                                </div>
                            </div>
                            <div class="form-group">
                                <label  class="font-weight-bold" for="photo">Upload Photo</label>
                                <input name="photo" class="form-control-file" type="file">
                            </div><br>
                            <button type="submit" style="height:45px; width:200px; border-radius:10px;" class="btn btn-success">Register</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </body>
</template>

<script>
export default{
   data() {
        return {
            csrf_token: '',
            message: '',
            errors: [],
            success:[]
        }
    },
    methods: {
        registerUser: function(){
            let registerForm= document.getElementById('registerForm');
            let router =this.$router;
            let form_data=new FormData(registerForm);
            let self=this;
            fetch("/api/register", {
                method: "POST",
                body: form_data,
                headers: {
                    'X-CSRFToken': this.csrf_token
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
                if ('message' in jsonResponse ){
                    self.success = 'Registration Succesful!';
                    self.message = 'success';
                    setTimeout(() => {
                        router.push('/login')
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