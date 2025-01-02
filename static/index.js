Vue.component('my-nav-bar', {
    props: ['navbar'],
    template: `
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item" v-for="el in navbar" :key="el.label">
                            <a class="nav-link text-dark" :href="el.url">{{ el.label }}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>`
  });
  
  Vue.component('my-hero', {
    data: function() {
        return  {
            members: [],
        }
    },
    methods: {
        getMembers() {
          const path = 'http://localhost:5000/members/';
          axios.get(path)
            .then((res) => {
              this.members = res.data.members;
              console.log(res.data)
            })
            .catch((error) => {
              console.error(error);
            });
        },
    },
    created() {
        this.getMembers();
    },
    template: `
        <div class="jumbotron container my-5 p-4 bg-light border rounded shadow">
            <h1 class="display-4 text-success">Liste des membres du Café des Sciences</h1>
            <p class="lead text-secondary">Cette liste représente les membres ayant leur cotisation à jour, pour l'année courante.</p>
            <hr class="my-4" />
            <p class="text-secondary">Pour toute question, me contacter à <strong>contact.laminutescientifique@gmail.com</strong>.</p>
            <div class="d-flex justify-content-center">
                <table class="table table-hover table-striped table-bordered w-auto text-center shadow-lg">
                    <thead class="table-success">
                        <tr>
                            <th scope="col">Nom</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(member, index) in members" :key="index">
                            <td>{{ member }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `
  });
  
  Vue.component('my-footer', {
    props: ['owner', 'site'],
    computed: {
        name() {
            site_owner = 'You'
            for(const property in this.owner) {
                if (property == 'name') {
                    site_owner = `${this.owner[property]}`;
                    break
                }
            }
            return site_owner;
        },
        website() {
            website = ''
            for(const property in this.owner) {
                if (property == 'website') {
                    website = `${this.owner[property]}`;
                    break
                }
            }
            return website;
        }
    },
    template: `
        <footer class="footer mt-auto py-3 bg-success text-light shadow">
            <div class="container text-center">
                <span class="fw-bold">🇫🇷 {{ name }}</span>
                <a :href="website" class="text-light ms-2" target="_blank"><small>{{ website }}</small></a>
            </div>
        </footer>
    `
  });
  
  
  const app = new Vue({
      el: '#app',
  })