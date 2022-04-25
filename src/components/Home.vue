<template>
    <div style="margin-top: -19px;">
        <div class="row no-gutters">
            <div class="col my-auto ">
                <div class="mx-auto" style="width:400px;">
                    <h1 class="font-weight-bold" style="font-size:50px;">Buy and Sell Cars Online</h1>
                    <br>
                    <p  style="font-size:17px;">United Auto Sales provides the fastest, easiest and most user friendly way to buy or sell cars online. Find a Great Price on the Vehicle You Want.</p>
                    <router-link style="width:150px;" type="button" class="btn btn-primary btn-lg rounded" to="/register">Register<span class="sr-only">(current)</span></router-link>
                    <router-link style="width:150px; margin-left :15px" type="button" class="btn btn-info btn-lg rounded" to="/login">Login<span class="sr-only">(current)</span></router-link>
                </div>
            </div>
            <div class="col">
                <img src="/src/static/images/home.jpg" alt="Car" style="width:100%;height:98vh;">
            </div>
        </div>
    </div>
</template>

<script>
export default{
    data(){
        return {}
    }
}
</script>
