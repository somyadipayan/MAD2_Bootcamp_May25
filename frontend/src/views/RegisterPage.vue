<template>

    <div class="container mt-5">
        <h2 class="text-center mb-4">Register Page</h2>
        <div class="my-form bg-light p-4 rounded shadow">
            <form @submit.prevent="register">
                <div class="form-group mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" v-model="name" class="form-control" id="name" required>
                </div>
                <div class="form-group mb-3">
                    <label for="email" class="form-label">Email address</label>
                    <input type="email"  v-model="email" class="form-control" id="email" aria-describedby="emailHelp" required>
                    <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                </div>
                <div class="form-group mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" v-model="password" class="form-control" id="password">
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            name: '',
            email: '',
            password: ''
        }
    }, 
    methods: {
        async register(){
        try{
            const response = await fetch('http://127.0.0.1:5000/register', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify({
                   name: this.name,
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
               this.$router.push('/')
            //    this.$router.push('/login')
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
