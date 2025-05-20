<template>
    <NavBar />
    <div class="container mt-5">
        <h2 class="text-center mb-4">Create Section</h2>
        <div class="my-form bg-light p-4 rounded shadow">
            <form @submit.prevent="editSection">
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
    name: 'EditSection',
    components: {
        NavBar
    },
    data() {
        return {
            section: {
                name: '',
                description: ''
            }
        }
    },
    async created() {
        const id = this.$route.params.id
        await this.getSection(id)
    },
    methods: {
        async getSection(id) {
            const response = await fetch('http://127.0.0.1:5000/sections/' + id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data = await response.json()
            if (response.ok) {
                this.section.name = data.section.name
                this.section.description = data.section.description
            } else {
                alert(data.error)
            }
        },
        async editSection() {
            const id = this.$route.params.id
            const response = await fetch('http://127.0.0.1:5000/sections/' + id, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: JSON.stringify(this.section)
            })
            const data = await response.json()
            if (response.ok) {
                alert(data.message)
                this.$router.push('/sections')
            } else {
                alert(data.error)
            }
        }
    }
}
</script>
