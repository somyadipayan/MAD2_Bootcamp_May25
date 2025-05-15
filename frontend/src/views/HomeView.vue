<template>
  <NavBar/>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Bootcamp"/>
    <p v-if="user">Hello {{user.name}}</p>
    <button @click="logout">Logout</button>
    
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import NavBar from '@/components/NavBar.vue';
import userMixin from '@/mixins/userMixin';

export default {
  name: 'HomeView',
  components: {
    HelloWorld,
    NavBar
  },
  mixins: [userMixin]
}
</script>
