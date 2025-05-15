export default{
    data(){
        return {
            user: null,
            loggedin : false,
            librarian : false
        }
    },
    async created(){
        await this.userStatus()
    },
    methods: {
        async userStatus(){
            const access_token = localStorage.getItem('access_token')
            if (!access_token){
                this.loggedin = false
                this.user = null
                this.librarian = false
                return;
            }
            this.user = await this.getUserInfo(access_token)
            if (this.user){
                this.loggedin = true
                this.librarian = this.user.librarian
            }
        },
        async getUserInfo(access_token){
            const response = await fetch('http://127.0.0.1:5000/get-user-info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
            })
            if(!response.ok){
                this.loggedin = false
                return null
            }
            const data = await response.json()
            return data.user
        },
        async logout(){
            console.log("I am inside logout function")
            const response = await fetch('http://127.0.0.1:5000/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data = await response.json()
            if(response.ok){
                localStorage.removeItem('access_token')
                this.user = null
                this.loggedin = false
                this.librarian = false
                this.$router.push('/login') 
            }
        }
    }
}