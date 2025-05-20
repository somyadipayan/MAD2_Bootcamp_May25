<template>
<NavBar/>
<div class="container mt-5">
    <h2 class="text-center mb-4">Add Book</h2>
    <div class="my-form bg-light p-4 rounded shadow">
        <form @submit.prevent="addBook">
            <div class="form-group mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" v-model="book.name" class="form-control" id="name" required>
            </div>
            <div class="form-group mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" v-model="book.description" id="description" rows="3"></textarea>
            </div>
            <div class="form-group mb-3">
                <label for="author" class="form-label">Author</label>
                <input type="text" v-model="book.author" class="form-control" id="author" required>
            </div>
            <div class="form-group mb-3">
                <label for="section" class="form-label">Section</label>
                <select class="form-control" v-model="book.section_id" id="section">
                    <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
                </select>
            </div>
            <div class="form-group mb-3">
                <label for="pdf" class="form-label">PDF</label>
                <input type="file" v-model="book.pdf" class="form-control" id="pdf" @change="handleFileUpload">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
    name: 'AddBook',
    data() {
        return {
            sections: [],
            book: {
                name: '',
                description: '',
                author: '',
                section_id: this.$route.query.section_id || '',
                pdf: null
            }   
        }
    },
    components: {
        NavBar
    },
    created() {
        this.getSections();
    },
    
    methods: {
         async getSections() {
            const response = await fetch('http://127.0.0.1:5000/sections', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data = await response.json()
            this.sections = data.sections
            console.log(this.sections)
        },

        async addBook() {
            try {
                const formData = new FormData();
                formData.append('name', this.book.name);
                formData.append('content', this.book.content);
                formData.append('author', this.book.author);
                formData.append('section_id', this.book.section_id);
                formData.append('pdf', this.book.pdf);
                
                const response = await fetch('http://127.0.0.1:5000/add-book', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                    },
                    body: formData
                });

                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    this.$router.push('/sections');
                } else {
                    alert(data.error);
                }

            } catch (error) {
                console.error(error);
            }
        },
        handleFileUpload(event) {
            this.book.pdf = event.target.files[0];
        }
    }
}
</script>