<template>
    <NavBar />
    <div class="container mt-5">
        <h2 class="text-center mb-4">Create Section</h2>
        <div class="my-form bg-light p-4 rounded shadow">
            <form @submit.prevent="createSection">
                <div class="form-group mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" v-model="section.name" class="form-control" id="name" required>
                </div>
                <div class="form-group mb-3">
                    <label for="description" class="form-label">Description</label>
                    <textarea class="form-control" v-model="section.description" id="description" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
    name: 'CreateSection',
    data() {
        return {
            section: {
                name: '',
                description: ''
            }
        }
    },
    components: {
        NavBar
    },
    methods: {
        async createSection() {
            const response = await fetch('http://127.0.0.1:5000/add-section', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: JSON.stringify(this.section)
            })
            const data = await response.json()
            if(!response.ok) {
                alert(data.error)
            }
            else {
                alert(data.message)
                this.$router.push('/sections')
            }
        }
    }
}
</script>