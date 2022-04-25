<template>
</template>
<script>
export default{
    data() {
        return {
            csrf_token: '',
        }
    },
    mounted: function(){
        let router =this.$router;
        fetch("/api/auth/logout", {
            method: "GET",
            headers: {
                'X-CSRFToken': this.csrf_token,
                'Authorization': "Bearer "+ localStorage.getItem("token")
            },
            credentials: 'same-origin'
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            if ('message' in jsonResponse ){
                localStorage.removeItem('token');
                localStorage.removeItem('id');
                self.success =  jsonResponse.message.message;
                self.message = 'success';
                router.push('login');
                console.log(jsonResponse);
            } else if ('errors' in jsonResponse ){
                console.log(jsonResponse);
                self.errors = jsonResponse.errors.errors;
                self.message = 'error';
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
    },
    created() {
        this.getCsrfToken();
    },
}
</script>