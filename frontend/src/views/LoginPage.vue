<template>
    <NavBar />
    <div class="container mt-5">
        <h2 class="text-center mb-4">Login Here</h2>
        <div class="my-form bg-light p-4 rounded shadow">
            <form @submit.prevent="login">
                <div class="form-group mb-3">
                    <label for="email" class="form-label">Email address</label>
                    <input type="email"  v-model="email" class="form-control" id="email" required>
                </div>
                <div class="form-group mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" v-model="password" class="form-control" id="password">
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
            </form>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
    data(){
        return {
            email: '',
            password: ''
        }
    },
    components: {
        NavBar
    },
    methods: {
        async login(){
        try{
            const response = await fetch('http://127.0.0.1:5000/login', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify({
                   email: this.email,
                   password: this.password
               })
           })
           const data = await response.json()
           if(!response.ok){
               alert(data.error)
           }
           else{
               alert(data.message)
               localStorage.setItem('access_token', data.access_token)
               this.$router.push('/')
           }
        }
        catch(error){
            console.log(error)
        }
        }
    }
}
</script>

<style scoped>
.my-form {
    max-width: 500px;
    margin: 0 auto
}
</style>
