<template>
    <body style="">
        <div class="d-flex align-items-center justify-content-center h-100"  style="margin-top:-40px;" >
            <div class="">
            <h2 class="font-weight-bold text-center" >Login to your account</h2>
            <br>
            <form @submit.prevent="loginUser" id="loginForm">
                <div id = "message">
                    <p class="alert alert-success" v-if="message === 'success'" >{{success}}</p>
                    <ul class="alert alert-danger" v-if="message === 'error'" >
                        <li v-for="errors in errors" :key="errors"> {{errors}}</li>
                    </ul> 
                </div>
                <div class="card p-3 mb-5" style="width: 30rem; border-radius:10px;">
                    <div class="card-body">
                    <div class="form-group">
                        <label class="font-weight-bold" for="username">Username</label>
                        <br>
                        <input name="username" style="height:50px; border-radius:10px;" class="form-control " type="text">
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold" for="password">Password</label>
                        <input name="password" autocomplete="on"  style="height:50px;  border-radius:10px; " class="form-control " type="password">
                    </div>
                    <br>
                    <button type="submit" style="height:40px; border-radius:10px;" class="btn btn-success w-100">Login</button>
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
        loginUser: function(){
            let loginForm= document.getElementById('loginForm');
            let router =this.$router;
            let form_data=new FormData(loginForm);
            let self=this;
            fetch("/api/auth/login", {
                method: "POST",
                body: form_data,
                headers: {
                    'X-CSRFToken': this.csrf_token
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                // console.log(response)
                return response.json();
            })
            .then(function (jsonResponse) {
                if ('message' in jsonResponse ){
                    let jwt_token=jsonResponse.message.token
                    localStorage.setItem("token",jwt_token)
                    localStorage.setItem("id",jsonResponse.message.id)
                    self.success =  jsonResponse.message.message;
                    self.message = 'success';
                    router.push('/explore')
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