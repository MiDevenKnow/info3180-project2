<template>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background-color:#202938;">
    <span class=" pl-2 pr-3"><img src="https://img.icons8.com/material-rounded/24/ffffff/car.png"/></span>  
    <a class="navbar-brand" href="#">United Auto Sales</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">

          <li class="nav-item active">
          <router-link class="nav-link" v-if="!link_status" to="/" >Home <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item active">
          <router-link class="nav-link " style="margin-left:200px;" v-if="link_status" to="/cars/new">Add Car <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item active">
          <router-link class="nav-link ml-4" v-if="link_status" to="/explore">Explore <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item active">
          <router-link class="nav-link ml-4" v-if="link_status" @click="profile_page()" v-bind:to="'/users/' + userid">My Profile <span class="sr-only">(current)</span></router-link>
          </li>
        </ul>
        <ul class="navbar-nav">
            <li class="nav-item active">
            <router-link class="nav-link"  v-if="!link_status" to="/register">Register <span class="sr-only">(current)</span></router-link>
            </li>
            <li class="nav-item active">
            <router-link class="nav-link"  v-if="!link_status" to="/login">Login <span class="sr-only">(current)</span></router-link>
            </li>
            <li class="nav-item active">
            <router-link class="nav-link" v-if="link_status" to="/logout">Logout<span class="sr-only">(current)</span></router-link>
            </li>
      </ul>
      </div>
    </nav>
</template>

<script>
export default{
    data: function(){
        return {
            userid: 0,
            link_status:false
        }
    }, 
    methods:{
        profile_page(){
            //location.reload();
        }
    },
    mounted: function(){
        let self=this;
        self.userid=localStorage.getItem('id');
        setInterval(()=>{
            if(localStorage.hasOwnProperty('token')){
                this.link_status=true;
            }
            else{
                this.link_status=false;
            }
        },1)
    }
}
</script>