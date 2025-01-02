Vue.component('my-nav-bar', {
    props: ['site'],
    data: function() {
        return  {
            search: '',
        }
    },
    methods: {
        searchMe: function () {
            console.log(this.search)
        }
    },
    computed: {
        logo() {
            site_logo = 'MySite'
            for(const property in this.site) {
                if (property == 'logo') {
                    site_logo = `${this.site[property]}`;
                    break;
                }
            }
            return site_logo;
        }
    },
    template: `
        <nav class="navbar navbar-light bg-light">
            <div class="container-fluid">
                <a class="navbar-brand bg-success p-1 text-light shadow">{{ logo }}</a>
                <form class="d-flex" v-on:submit.prevent="searchMe">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="search" />
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </nav>
    `
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
      <div class="jumbotron container m-5">
          <h1 class="display-4">Hello, world!</h1>
          <p class="lead">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book</p>
          <hr class="my-4" />
          <p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.</p>
          <p class="lead">
              <a class="btn btn-success btn-lg" href="wilber.co.ke" role="button">Learn more</a>
          </p>
            <div class="d-flex justify-content-center">
            <table class="table table-hover w-auto">
            <thead>
                <tr>
                <th scope="col">Name</th>
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
      <footer class="footer mt-auto py-3 bg-light">
          <div class="container">
              <span class="text-muted mx-2"><strong>🇰🇪 {{ name }}</strong></span>
              <a href=""><small>{{ website }}</small></a>
          </div>
      </footer>
    `
  });
  
  
  const app = new Vue({
      el: '#app',
  })