/* Add your Application JavaScript */

// NOTE: //
// STORE FLASH MESSAGE AS JSON.stringify({flash: [message, isSuccess]}) // where isSuccess determines color

function loginNav(){
  document.getElementById('logged-in').classList.remove('d-none');
  document.getElementById('user-menu').classList.remove('d-none');
  document.getElementById('navbar').classList.remove('d-none');
  document.getElementById('navbar').classList.add('d-flex');
  document.getElementsByTagName('body')[0].style.backgroundColor = 'var(--whitespace)';
}

function logoutNav(){
  document.getElementById('logged-in').classList.add('d-none');
  document.getElementById('user-menu').classList.add('d-none');
  document.getElementById('navbar').classList.add('d-none');
  document.getElementById('navbar').classList.remove('d-flex');
  document.getElementsByTagName('body')[0].style.backgroundColor = 'rgba(25, 62, 97,0.1)';
}

function isLoggedIn(){
  return sessionStorage.getItem('jets_token');
}

function flashMessage(obj, success=true) {
  if (obj.flashMessage){
    obj.displayFlash = true;
    obj.isSuccess = success;
    setTimeout(function() { 
      obj.displayFlash = false;
        sessionStorage.removeItem('flash')
    }, 3000);
  }
}

const Register = {
  name: 'Register',
  template: `
      <div class="container col-md-8 offset-md-2" id="registration-page">
        <transition name="fade" class="mt-5">
          <div v-if="displayFlash" v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]" class="alert">
              {{ flashMessage }}
          </div>
        </transition>
        <h1 class="font-weight-bold registration-header mt-4">Register New User</h1>
        <form method="post" @submit.prevent="register_user" id="registration-form" class="w-100 mt-3">
            <div class="form-row">  
                <div class="form-group col-md-6 sm-padding-right">
                    <label for="username">TRN</label><br>
                    <input type="text" name="username" class='form-control' required/> 
                </div>
                <div class="form-group col-md-6">
                    <label for="password">Password</label><br>
                    <input type="password" name="password" class='form-control' required/>
                </div>
            </div>
        </form>
      </div>
  `,
  data(){
    return {
      user_data: '',
      flashMessage: sessionStorage.getItem('flash'),
      displayFlash: false,
      isSuccess: false,
      alertSuccessClass: 'alert-success',
      alertErrorClass: 'alert-danger'
    }
  },
  created() {
    if (isLoggedIn()){
      console.log('Please logout to register an account.');
      this.$router.push('/notifications');
    } else {
      logoutNav();
    }
  },
  methods: {
    register_user() {
      let form = document.getElementById('registration-form');
      let form_data = new FormData(form);
      let self = this;
      fetch("/api/register", {
          method: 'POST',
          body: form_data,
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      })
      .then(function (jsonResponse) {
        if (jsonResponse['error']){
          self.displayFlash = true;
          self.flashMessage = jsonResponse['error'];
          setTimeout(function() { 
              self.displayFlash = false;
          }, 3000);
        } else if(jsonResponse['licensePlate'][0][0] === '.' ){
          self.displayFlash = true;
          self.flashMessage = jsonResponse['licensePlate'][0];
          setTimeout(function() { 
              self.displayFlash = false;
          }, 3000);
        } else {
            self.$router.push('/login');
            self.user_data = jsonResponse;
            sessionStorage.setItem('jets_user', JSON.stringify(jsonResponse['id']));
            sessionStorage.setItem('flash','Registered successfully');
        }
          console.log(jsonResponse);
      })
      .catch(function (error) {
          console.log(error);
      });
    }
  }
};

const Login = {
  name: 'Login',
  template: `
    <div class="container login-page d-flex justify-content-center w-100">
      <div class='d-flex login-frame'>
          <section id='sign-in-section' class='p-4'>
            <img src="/static/assets/favicon.svg" alt="JETS Logo">
            <span class='jets-name ml-3'>JETS</span>

            <transition name="fade" class="mt-3">
              <div v-if="displayFlash" v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]" class="alert">
                  {{ flashMessage }}
              </div>
            </transition>

            <form method="post" @submit.prevent="login_user" id="loginForm" class="d-flex flex-column">
              <h1 class="sign-in-text mb-4">Sign in</h1>
              <div class="form-group">
                <label for="username" class="mt-2">Username</label>
                <input type="text" name="username" class='form-control' id='usernameField' required/> 
              </div>
              <div class="form-group ml-5">
                <label for="password" class="mt-3">Password</label>
                <input type="password" name="password" class='form-control' required/> 
              </div>
              <button type="submit" name="submit-btn" class="btn submit-button py-1 mx-auto mt-3">Sign in</button>
            </form>
          </section>
          <section id='app-name-section' class='d-flex justify-content-center'>
            <div class='d-flex flex-column justify-content-center'>
              <div class='login-app-name d-flex justify-content-end'>JamaicaEye</div>
              <div class='login-app-name d-flex justify-content-end'>Ticketing</div>
              <div class='login-app-name d-flex justify-content-end'>System</div>
            </div>
          </section>
      </div>
      
    </div>
  `,
  created(){
    if (isLoggedIn()){
      console.log('You are already logged in.');
      sessionStorage.setItem('flash','You are already logged in')
      this.$router.push('/');
    } else {
      logoutNav();
      flashMessage(this);
    }
  },
  data(){
    return {
      flashMessage: sessionStorage.getItem('flash'),
      displayFlash: false,
      isSuccess: false,
      alertSuccessClass: 'alert-success',
      alertErrorClass: 'alert-danger'
    }
  },
  methods: {
    login_user() {
      let loginForm = document.getElementById('loginForm');
      let form_data = new FormData(loginForm);
      let self = this;
      fetch("/api/auth/login", {
          method: 'POST',
          body: form_data,
          headers: {
              'X-CSRFToken': csrf_token
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
          if (!response.ok) {
            throw Error(response.statusText);
          }
          return response.json();
      })
      .then(function (jsonResponse) {
          if (jsonResponse['token']){
            if (typeof(Storage) !== "undefined") {
              sessionStorage.setItem('jets_token', jsonResponse['token']);
              sessionStorage.setItem('jets_user', JSON.stringify(jsonResponse['user']));
            } else {
              console.log('No Web Storage support..');
            }
            self.$router.push('/flagged');
            sessionStorage.setItem('flash',jsonResponse['message']);
            document.getElementById('username').innerHTML = jsonResponse['user'].name
          } else {
            if(jsonResponse['error']){
              self.displayFlash = true;
              self.flashMessage = jsonResponse['error'];
              setTimeout(function() { 
                self.displayFlash = false;
              }, 3000);
            } /*else if(jsonResponse['username']){
              self.flashMessage = jsonResponse['username'][0];
            } else if(jsonResponse['password']){
              self.flashMessage = jsonResponse['password'][0];
            }*/
            
          }
          console.log(jsonResponse);
      })
      .catch(function (error) {
          console.log(error);
      });
    }
  }
};

const Logout = {
  name: 'Logout',
  template: `
  `,
  created(){
    if (!isLoggedIn()){
      this.$router.push('/login')
      return;
    }
    let self = this;
    fetch("/api/auth/logout", {
      method: 'POST',
      headers: {
          'X-CSRFToken': csrf_token,
          'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
      },
      credentials: 'same-origin'
    })
    .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
    })
    .then(function (jsonResponse) {
        self.$router.push('/login');
        sessionStorage.removeItem('jets_token');
        sessionStorage.removeItem('jets_user');
        sessionStorage.removeItem('flash');
        self.message = jsonResponse['message'];
    })
    .catch(function (error) {
        console.log(error);
    });
  },
  data() {
      return {
        message: ''
      }
  },
  methods: {
  }
};

const Offenders = {
  name: 'Offenders',
  template: `
    <div id="offenders-page-container" class="">

      <div class='controls-container d-flex justify-content-between pt-3'>
        <search-bar></search-bar>
        <transition name="fade" class="mt-5">
          <div v-if="displayFlash" v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]" class="alert">
              {{ flashMessage }}
          </div>
        </transition>
        <div class='buttons d-flex'>
          <simulate-btn @click=simulateOffender></simulate-btn>
          <reset-btn @click='resetSimulation' class='ml-4'></reset-btn>
        </div>
      </div>
      <h3 class='mt-3'><b>Traffic Offenders</b></h3>
      <table class="table mt-4" id="offenders-table">
        <caption class="sr-only">List of offenders</caption>
        <thead>
          <tr>
            <th scope="col">Vehicle Owner</th>
            <th scope="col">Date & Time</th>
            <th scope="col">Offence Desc.</th>
            <th scope="col">Registration #</th>
            <th scope="col">Location</th>
          </tr>
        </thead>

        <tbody v-if='tickets.length > 0' id='offenders-table-body'>
          <tr v-for='ticket in tickets' @click="viewTicket(ticket.id)">
            <td>{{ticket.vehicleOwner.fname}} {{ticket.vehicleOwner.lname}}</td>
            <td>{{ticket.incident.date}} {{ticket.incident.time}}</td>
            <td>{{ticket.offence.description}}</td>
            <td>{{ticket.vehicle.licenseplate}}</td>
            <td>{{ticket.location.description}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    `,
  data() {
      return {
        tickets: [],
        flashMessage: sessionStorage.getItem('flash'),
        displayFlash: false,
        isSuccess: false,
        alertSuccessClass: 'alert-success',
        alertErrorClass: 'alert-danger'
      }
  },
  created() {
    if (isLoggedIn()){
      loginNav();
      this.$router.push('/issued');
      flashMessage(this);
    } else {
      logoutNav();
      this.$router.push('/login');
    }
    this.fetchOffenders();
  },
  methods: {
    fetchOffenders() {
      let self = this;
      fetch("/api/issued", {
          fetchOffenders: 'GET',
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      })
      .then(function (offenceData) {
        console.log(offenceData);
        offenceData.forEach((ticket, index) => {
          if(ticket['status'] === 'IMAGE PROCESSING ERROR' || ticket['status'] === 'NO EMAIL ADDRESS ON FILE' ){
            console.log('PUSH TO NOTIFICATIONS');
            this.$router.push(`/flagged`);
          } else {
            console.log(ticket);
            self.updateTable(ticket);
          }
        })
      })
      .catch(function (error) {
          console.log(error);
      });
    },
    simulateOffender() {
      let self = this;
      fetch("/api/simulate", {
          method: 'GET',
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      })
      .then(function (offenceData) {
        if(offenceData['id'] !== '#'){
          console.log('SIMULATED');
          if(offenceData['status'] === 'IMAGE PROCESSING ERROR' || offenceData['status'] === 'NO EMAIL ADDRESS ON FILE' ){
              console.log('PUSHED TO NOTIFICATIONS');
              self.$router.push(`/flagged`);
          } else {
              console.log(`TICKET STATUS: ${offenceData['status']}`);
              self.updateTable(offenceData);
          }
          console.log(offenceData);
        } else {
          console.log('NO MORE IMAGES TO SERVE');
        }
      })
      .catch(function (error) {
          console.log(error);
      });
    },
    viewTicket(ticketID){
      this.$router.push(`/issued/${ticketID}`);
    },
    updateTable(offenceData){
      this.tickets.unshift(offenceData);
    },
    resetSimulation(){
      let self = this;
      fetch("/api/resetSimulation", {
          method: 'GET',
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      })
      .then(function (status) {
          console.log(status['message']);
          self.$router.push(`/`);
      })
      .catch(function (error) {
          console.log(error);
      });
    }
  }
};

const Notifications = {
  name: 'Notifications',
  template: `
    <div id="notifications-page-container" class="">
      <transition name="fade" class="mt-5">
        <div v-if="displayFlash" v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]" class="alert">
            {{ flashMessage }}
        </div>
      </transition>
      <div class='controls-container d-flex justify-content-between pt-3'>
        <search-bar></search-bar>
        <!--<simulate-btn @click=simulateOffender></simulate-btn>-->
      </div>
      <h3 class='mt-3'><b>Notifications</b></h3>
      <table class="table mt-4" id="notifications-table">
        <caption class="sr-only">Notifications Table</caption>
        <thead>
          <tr>
            <th scope="col">Vehicle Owner</th>
            <th scope="col">Date & Time</th>
            <th scope="col">Offence Desc.</th>
            <th scope="col">Registration #</th>
            <th scope="col">Location</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody v-if='tickets.length > 0' id='notifications-table-body'>
          <tr v-for='ticket in tickets' @click="viewTicket(ticket.id, ticket.status)">
            <td>{{ticket.vehicleOwner.fname}} {{ticket.vehicleOwner.lname}}</td>
            <td>{{ticket.incident.date}} {{ticket.incident.time}}</td>
            <td>{{ticket.offence.description}}</td>
            <td>{{ticket.vehicle.licenseplate}}</td>
            <td>{{ticket.location.description}}</td>
            <td>{{ticket.status}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    `, data() {
      return {
        tickets: [],
        flashMessage: sessionStorage.getItem('flash'),
        displayFlash: false,
        isSuccess: false,
        alertSuccessClass: 'alert-success',
        alertErrorClass: 'alert-danger'
      }
  },
  created() {
    if (isLoggedIn()){
      loginNav()
      this.fetchOffenders();
      this.$router.push('/flagged');
      flashMessage(this);
    }
    else {
      logoutNav();
      this.$router.push('/login');
    }
  },
  methods: {
    fetchOffenders() {
      let self = this;
      fetch("/api/flagged", {
          fetchOffenders: 'GET',
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      })
      .then(function (offenceData) {
        console.log(offenceData)  
        offenceData.forEach((ticket, index) => {
          if(ticket['status'] === 'ISSUED (EMAIL)' ){
            console.log('PUSHED TO TRAFFIC OFFENDERS');
            this.$router.push(`/issued`);
          } else {
            console.log(ticket);
            self.updateTable(ticket);
          }
        })

      })
      .catch(function (error) {
          console.log(error);
      });
    },
    viewTicket(ticketID,status){
      this.$router.push(`/flagged/${ticketID}/${status}`);
    },
    updateTable(offenceData){
      this.tickets.unshift(offenceData);
    }
  }
};

const ViewIssued = {
  name: 'ViewIssued',
  template: `
    <div id="ticket-page-container" class="mt-5">
      <div class="controls d-flex justify-content-end pt-2">
        <!--<issue-btn></issue-btn>-->
        <!--<archive-btn class='ml-3'></archive-btn>-->
        <print-btn id='print-btn' class='ml-3' @click=printTicket></print-btn>
      </div>
      <div id='issued-ticket-status' class='status-bar rounded-top mt-5 d-flex align-items-center'>
        <h2 class='mb-0 py-2'>{{ticket.status}}</h2>
      </div>
      <div class="ticket">
        <div class='ticket-header d-flex align-items-center pb-2'>
          <img src="/static/assets/coat_of_arms.png" alt="Coat of Arms" class='rounded'>
          <div class='ticket-header-headings d-flex flex-column'>
            <h1 class='mb-0'>ELECTRONIC TRAFFIC VIOLATION TICKET</h1>
            <h2 class=''>JAMAICA CONSTABULARY FORCE</h2>
          </div>
        </div>
        <section>
          <h3>VEHICLE OWNER INFORMATION</h3>
          <div class='ticket-rows owner'>
            <div class='ticket-row drivers-license'>
              <div class='ticket-field'>
                <h4 class='field-name'>Driver's License Number</h4>
                <p class='field-value'>{{ticket.vehicleOwner.trn}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Expiration Date</h4>
                <p class='field-value'>{{ticket.vehicleOwner.expdate}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Type</h4>
                <p class='field-value'>{{ticket.vehicleOwner.licenseType}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Licensed In</h4>
                <p class='field-value'>{{ticket.vehicleOwner.licensein}}</p>
              </div>
            </div>

            <div class='ticket-row bio'>
              <div class='ticket-field'>
                <h4 class='field-name'>Last Name</h4>
                <p class='field-value'>{{ticket.vehicleOwner.lname}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>First Name</h4>
                <p class='field-value'>{{ticket.vehicleOwner.fname}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Middle Name</h4>
                <p class='field-value'>{{ticket.vehicleOwner.mname}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Date of Birth</h4>
                <p class='field-value'>{{ticket.vehicleOwner.dob}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Gender</h4>
                <p class='field-value'>{{ticket.vehicleOwner.gender}}</p>
              </div>
            </div>

            <div class='ticket-row address'>
              <div class='ticket-field'>
                <h4 class='field-name'>Address</h4>
                <p class='field-value'>{{ticket.vehicleOwner.address}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Country</h4>
                <p class='field-value'>{{ticket.vehicleOwner.country}}</p>
              </div>
              <div class='ticket-field parish-residence'>
                <h4 class='field-name'>Parish</h4>
                <p class='field-value'>{{ticket.vehicleOwner.parish}}</p>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h3>VEHICLE INFORMATION</h3>
          <div class='ticket-rows'>
            <div class='ticket-row vehicle vehicle-1'>
              <div class='ticket-field'>
                <h4 class='field-name'>Type of Vehicle</h4>
                <p class='field-value'>{{ticket.vehicle.cartype}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Registration Plate No.</h4>
                <p class='field-value'>{{ticket.vehicle.licenseplate}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>License Disc No.</h4>
                <p class='field-value'>{{ticket.vehicle.licensediscno}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Expiration Date</h4>
                <p class='field-value'>{{ticket.vehicle.expdate}}</p>
              </div>
            </div>

            <div class='ticket-row vehicle vehicle-2'>
              <div class='ticket-field'>
                <h4 class='field-name'>Year</h4>
                <p class='field-value'>{{ticket.vehicle.year}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Make</h4>
                <p class='field-value'>{{ticket.vehicle.make}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Model</h4>
                <p class='field-value'>{{ticket.vehicle.model}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Colour</h4>
                <p class='field-value'>{{ticket.vehicle.colour}}</p>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h3>OFFENCE INFORMATION</h3>
          <div class='ticket-rows offence'>
            <div class='ticket-row offence-1'>
              <div class='ticket-field'>
                <h4 class='field-name'>Date of Offence</h4>
                <p class='field-value'>{{ticket.incident.date}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Time of Offence</h4>
                <p class='field-value'>{{ticket.incident.time}}</p>
              </div>
              <div class='ticket-field parish-offence'>
                <h4 class='field-name'>Parish of Offence</h4>
                <p class='field-value'>{{ticket.location.parish}}</p>
              </div>
            </div>

            <div class='ticket-row offence-2'>
              <div class='ticket-field offence-location'>
                <h4 class='field-name'>Location of Offence</h4>
                <p class='field-value'>{{ticket.location.description}}</p>
              </div>
              <div class='ticket-field offence-desc'>
                <h4 class='field-name'>Description of Offence</h4>
                <p class='field-value'>{{ticket.offence.description}}</p>
              </div>
            </div>

            <div class='ticket-row tax-auth'>
              <div class='ticket-field'>
                <h4 class='field-name'>Fine</h4>
                <p class='field-value'>&#36{{ticket.offence.fine}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Points Assigned</h4>
                <p class='field-value'>{{ticket.offence.points}}</p>
              </div>
              <div class='ticket-field payment-deadline'>
                <h4 class='field-name'>Payment Deadline</h4>
                <p class='field-value'>{{ticket.incident.paymentDeadline}}</p>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h3>TRAFFIC CAM SNAPSHOT</h3>
          <div id='snapshot-container'>
            <img :src="ticket.incident.image" alt='offender snapshot' class=''/>
          </div>
          <div class='ticket-row official-use'>
            <div class='ticket-field'>
              <h4 class='field-name'>Traffic Ticket No.</h4>
              <p class='field-value'>{{ticket.id}}</p>
            </div>
            <div class='ticket-field'>
              <h4 class='field-name'>Date Issued</h4>
              <p class='field-value'>{{ticket.dateIssued}}</p>
            </div>
            <div class='ticket-field'>
              <h4 class='field-name'>Status</h4>
              <p class='field-value'>{{ticket.status}}</p>
            </div>
          </div>
        </section>
      </div>

    </div>
  `,
  data() {
      return {
        ticket: {
          'vehicleOwner': '',
          'vehicle': '',
          'offence': '',
          'incident': '',
          'location': '',
          'status': '',
          'dateIssued': '',
          'id': ''
        },
        user: sessionStorage.getItem('jets_user'),
        flashMessage: sessionStorage.getItem('flash'),
        displayFlash: false,
        isSuccess: false,
        alertSuccessClass: 'alert-success',
        alertErrorClass: 'alert-danger'
      }
  },
  created(){
    /*if (!isLoggedIn()){
      this.$router.push('/login');
      return;
    }*/
    loginNav();
    let self = this;
    //self.offender = sessionStorage.getItem('selected_offender')
    self.fetchOffender(self);
    //flashMessage(self);
  },
  methods: {
    fetchOffender(self){
      fetch(`/api/issued/${this.$route.params.ticketID}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrf_token,
            'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
        },
        credentials: 'same-origin'
      })
      .then(function (response) {
        return response.json();
        })
      .then(function (response) {
        self.ticket = response;
        console.log(response)    
      })
    },
    printTicket(self){
        // Make navbar and footer invisible
        document.getElementById('navbar').classList.add('d-none');
        document.getElementById('navbar').classList.remove('d-flex');
        document.getElementById('footer').classList.add('d-none');
        document.getElementById('print-btn').classList.add('d-none');
        document.getElementById('print-btn').classList.remove('d-flex');
        document.getElementById('issued-ticket-status').classList.add('d-none');
        document.getElementById('issued-ticket-status').classList.remove('d-flex');
        
        window.print()  // Print E-Ticket

        // Make navbar and footer Visible
        document.getElementById('navbar').classList.remove('d-none');
        document.getElementById('navbar').classList.add('d-flex');
        document.getElementById('footer').classList.remove('d-none');
        document.getElementById('print-btn').classList.remove('d-none');
        document.getElementById('print-btn').classList.add('d-flex');
        document.getElementById('issued-ticket-status').classList.remove('d-none');
        document.getElementById('issued-ticket-status').classList.add('d-flex');

    }
  }
};

const ViewFlagged = {
  name: 'ViewFlagged',
  template: `
    <div id="ticket-page-container" class="mt-5">
      <div class="controls d-flex justify-content-end pt-2">
        <issue-btn class='issue-btn'></issue-btn>
        <archive-btn class='archive-btn ml-3'></archive-btn>
        <print-btn id='print-btn' class='ml-3' @click=printTicket></print-btn>
      </div>
      <div id='flagged-ticket-status' class='status-bar rounded-top mt-5 d-flex align-items-center'>
        <h2 class='mb-0 py-2'>{{ticket.status}}</h2>
      </div>
      <div class="ticket">
        <div class='ticket-header d-flex align-items-center pb-2'>
          <img src="/static/assets/coat_of_arms.png" alt="Coat of Arms" class='rounded'>
          <div class='ticket-header-headings d-flex flex-column'>
            <h1 class='mb-0'>ELECTRONIC TRAFFIC VIOLATION TICKET</h1>
            <h2 class=''>JAMAICA CONSTABULARY FORCE</h2>
          </div>
        </div>
        <section>
          <h3>VEHICLE OWNER INFORMATION</h3>
          <div class='ticket-rows owner'>
            <div class='ticket-row drivers-license'>
              <div class='ticket-field'>
                <h4 class='field-name'>Driver's License Number</h4>
                <p class='field-value'>{{ticket.vehicleOwner.trn}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Expiration Date</h4>
                <p class='field-value'>{{ticket.vehicleOwner.expdate}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Type</h4>
                <p class='field-value'>{{ticket.vehicleOwner.licenseType}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Licensed In</h4>
                <p class='field-value'>{{ticket.vehicleOwner.licensein}}</p>
              </div>
            </div>

            <div class='ticket-row bio'>
              <div class='ticket-field'>
                <h4 class='field-name'>Last Name</h4>
                <p class='field-value'>{{ticket.vehicleOwner.lname}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>First Name</h4>
                <p class='field-value'>{{ticket.vehicleOwner.fname}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Middle Name</h4>
                <p class='field-value'>{{ticket.vehicleOwner.mname}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Date of Birth</h4>
                <p class='field-value'>{{ticket.vehicleOwner.dob}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Gender</h4>
                <p class='field-value'>{{ticket.vehicleOwner.gender}}</p>
              </div>
            </div>

            <div class='ticket-row address'>
              <div class='ticket-field'>
                <h4 class='field-name'>Address</h4>
                <p class='field-value'>{{ticket.vehicleOwner.address}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Country</h4>
                <p class='field-value'>{{ticket.vehicleOwner.country}}</p>
              </div>
              <div class='ticket-field parish-residence'>
                <h4 class='field-name'>Parish</h4>
                <p class='field-value'>{{ticket.vehicleOwner.parish}}</p>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h3>VEHICLE INFORMATION</h3>
          <div class='ticket-rows'>
            <div class='ticket-row vehicle vehicle-1'>
              <div class='ticket-field'>
                <h4 class='field-name'>Type of Vehicle</h4>
                <p class='field-value'>{{ticket.vehicle.cartype}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Registration Plate No.</h4>
                <p class='field-value'>{{ticket.vehicle.licenseplate}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>License Disc No.</h4>
                <p class='field-value'>{{ticket.vehicle.licensediscno}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Expiration Date</h4>
                <p class='field-value'>{{ticket.vehicle.expdate}}</p>
              </div>
            </div>

            <div class='ticket-row vehicle vehicle-2'>
              <div class='ticket-field'>
                <h4 class='field-name'>Year</h4>
                <p class='field-value'>{{ticket.vehicle.year}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Make</h4>
                <p class='field-value'>{{ticket.vehicle.make}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Model</h4>
                <p class='field-value'>{{ticket.vehicle.model}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Colour</h4>
                <p class='field-value'>{{ticket.vehicle.colour}}</p>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h3>OFFENCE INFORMATION</h3>
          <div class='ticket-rows offence'>
            <div class='ticket-row offence-1'>
              <div class='ticket-field'>
                <h4 class='field-name'>Date of Offence</h4>
                <p class='field-value'>{{ticket.incident.date}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Time of Offence</h4>
                <p class='field-value'>{{ticket.incident.time}}</p>
              </div>
              <div class='ticket-field parish-offence'>
                <h4 class='field-name'>Parish of Offence</h4>
                <p class='field-value'>{{ticket.location.parish}}</p>
              </div>
            </div>

            <div class='ticket-row offence-2'>
              <div class='ticket-field offence-location'>
                <h4 class='field-name'>Location of Offence</h4>
                <p class='field-value'>{{ticket.location.description}}</p>
              </div>
              <div class='ticket-field offence-desc'>
                <h4 class='field-name'>Description of Offence</h4>
                <p class='field-value'>{{ticket.offence.description}}</p>
              </div>
            </div>

            <div class='ticket-row tax-auth'>
              <div class='ticket-field'>
                <h4 class='field-name'>Fine</h4>
                <p class='field-value'>&#36{{ticket.offence.fine}}</p>
              </div>
              <div class='ticket-field'>
                <h4 class='field-name'>Points Assigned</h4>
                <p class='field-value'>{{ticket.offence.points}}</p>
              </div>
              <div class='ticket-field payment-deadline'>
                <h4 class='field-name'>Payment Deadline</h4>
                <p class='field-value'>{{ticket.incident.paymentDeadline}}</p>
              </div>
            </div>
          </div>
        </section>
        <section>
          <h3>TRAFFIC CAM SNAPSHOT</h3>
          <div id='snapshot-container'>
            <img :src="ticket.incident.image" alt='offender snapshot' class=''/>
          </div>
          <div class='ticket-row official-use'>
            <div class='ticket-field'>
              <h4 class='field-name'>Traffic Ticket No.</h4>
              <p class='field-value'>{{ticket.id}}</p>
            </div>
            <div class='ticket-field'>
              <h4 class='field-name'>Date Issued</h4>
              <p class='field-value'>{{ticket.dateIssued}}</p>
            </div>
            <div class='ticket-field'>
              <h4 class='field-name'>Status</h4>
              <p class='field-value'>{{ticket.status}}</p>
            </div>
          </div>
        </section>
      </div>

    </div>
  `,
  data() {
      return {
        ticket: {
          'vehicleOwner': '',
          'vehicle': '',
          'offence': '',
          'incident': '',
          'location': '',
          'status': '',
          'dateFlagged': '',
          'id': ''
        },
        user: sessionStorage.getItem('jets_user'),
        flashMessage: sessionStorage.getItem('flash'),
        displayFlash: false,
        isSuccess: false,
        alertSuccessClass: 'alert-success',
        alertErrorClass: 'alert-danger'
      }
  },
  created(){
    if (!isLoggedIn()){
      this.$router.push('/login');
      return;
    }
    loginNav();
    let self = this;
    //self.offender = sessionStorage.getItem('selected_offender')
    self.fetchOffender(self);
    //flashMessage(self);
  },
  methods: {
    fetchOffender(self){
      fetch(`/api/flagged/${this.$route.params.ticketID}/${this.$route.params.ticketStatus}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrf_token,
            'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
        },
        credentials: 'same-origin'
      })
      .then(function (response) {
        return response.json();
        })
      .then(function (response) {
        self.ticket = response;
        console.log(response)    
      })
    },
    printTicket(self){
        // Make navbar and footer invisible
        document.getElementById('navbar').classList.add('d-none');
        document.getElementById('navbar').classList.remove('d-flex');
        document.getElementById('footer').classList.add('d-none');
        document.getElementById('print-btn').classList.add('d-none');
        document.getElementById('print-btn').classList.remove('d-flex');
        document.getElementById('flagged-ticket-status').classList.add('d-none');
        document.getElementById('flagged-ticket-status').classList.remove('d-flex');
        document.getElementsByClassName('issue-btn')[0].classList.add('d-none');
        document.getElementsByClassName('issue-btn')[0].classList.remove('d-flex');
        document.getElementsByClassName('archive-btn')[0].classList.add('d-none');
        document.getElementsByClassName('archive-btn')[0].classList.remove('d-flex');
        
        window.print()  // Print E-Ticket

        // Make navbar and footer Visible
        document.getElementById('navbar').classList.remove('d-none');
        document.getElementById('navbar').classList.add('d-flex');
        document.getElementById('footer').classList.remove('d-none');
        document.getElementById('print-btn').classList.remove('d-none');
        document.getElementById('print-btn').classList.add('d-flex');
        document.getElementById('flagged-ticket-status').classList.remove('d-none');
        document.getElementById('flagged-ticket-status').classList.add('d-flex');
        document.getElementsByClassName('issue-btn')[0].classList.remove('d-none');
        document.getElementsByClassName('issue-btn')[0].classList.add('d-flex');
        document.getElementsByClassName('archive-btn')[0].classList.remove('d-none');
        document.getElementsByClassName('archive-btn')[0].classList.add('d-flex');

    }
  }
};

const ManualIssue = {
  name: 'ManualIssue',
  template: `

    <div class="container d-flex justify-content-center py-5">
      <div class='d-flex form-container flex-column'>
        <transition name="fade" class="mt-3">
          <div v-if="displayFlash" v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]" class="alert">
              {{ flashMessage }}
          </div>
        </transition>

        <form method="post" @submit.prevent="add_offender" id="manualIssueForm" class="mb-5 p-5 rounded border d-flex flex-column align-items-center">
          <h1 class="sign-in-text mb-4">Issue Ticket</h1>  
          <div class="form-group sm-padding-right">
            <label for="date"><span class='pr-2'>Date</span><span id='date-format'>(yyyy/mm/dd)</span></label><br>
            <input type="text" name="date" class='form-control' required/> 
          </div>
          <div class="form-group">
            <label for="time"><span class='pr-2'>Time</span><span id='time-format'>(hh:mm)</span></label><br>
            <input type="text" name="time" class='form-control' required/>
          </div>
        
          <div class="form-group sm-padding-right">
            <label for="location">Location</label><br>
            <input type="text" name="location" class='form-control' required/> 
          </div>
          <div class="form-group">
            <label for="parish">Parish</label><br>
            <select name="parish" id="parish" form="manualIssueForm" class="form-control">
              <option value="St. Andrew">St. Andrew</option>
              <option value="Kingston">Kingston</option>
              <option value="St. Catherine">St. Catherine</option>
              <option value="Clarendon">Clarendon</option>
              <option value="Manchester">Manchester</option>
              <option value="St. Elizabeth">St. Elizabeth</option>
              <option value="Westmoreland">Westmoreland</option>
              <option value="Hanover">Hanover</option>
              <option value="St. James">St. James</option>
              <option value="Trelawny">Trelawny</option>
              <option value="St. Ann">St. Ann</option>
              <option value="St. Mary">St. Mary</option>
              <option value="Portland">Portland</option>
              <option value="St. Thomas">St. Thomas</option>
            </select>
          </div>

          <div class="form-group sm-padding-right">
            <label for="Offence">Offence</label><br>
            <select name="offence" id="offence" form="manualIssueForm" class="form-control">
              <option value="E200">Exceeding the speed limit ( > 10kmph ) </option>
              <option value="E300">Exceeding the speed limit ( > 25kmph ) </option>
              <option value="E400">Exceeding the speed limit ( > 50kmph )</option>
              <option value="F100">Failure to obey traffic signal</option>
            </select>
          </div>
          <div class="form-group d-flex flex-column pl-3">
            <label for="snapshot">Snapshot</label>
            <input type="file" name="snapshot" required/> 
          </div>
          <button type="submit" name="submit-btn" class="btn submit-button py-1 mx-auto mt-3 w-50" style='color: white'>Submit</button>
        </form>
      </div>
    </div>
  `,
  data() {
      return {
        flashMessage: sessionStorage.getItem('flash'),
        displayFlash: false,
        isSuccess: false,
        alertSuccessClass: 'alert-success',
        alertErrorClass: 'alert-danger'
      }
  },
  created(){
    if (!isLoggedIn()){
      this.$router.push('/login')
      return;
    }
    loginNav();
    flashMessage(this);
  },
  methods: {
    add_offender(){
      let form = document.getElementById('manualIssueForm');
      let form_data = new FormData(form);
      let self = this;
      fetch("/api/issue", {
          method: 'POST',
          body: form_data,
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
          if (!response.ok) {
            sessionStorage.setItem('flash', "Offender could not be added")
            self.$router.push('/')
            throw Error(response.statusText);
          }
          return response.json();
      })
      .then(function (jsonResponse) {
          //self.offender_data = jsonResponse
          sessionStorage.setItem('flash', "Offender succesfully added")
          if (jsonResponse['status'].search('@') > 0) {
            self.$router.push('/issued')
          } else {
            self.$router.push('/')
          }
          
      })
      .catch(function (error) {
          console.log('Looks like there was a problem: \n', error);
      });
    }
  }
};

let searchQuery = ''  // Global variable for storing a search query entered on a route outside SearchResults

const SearchResults = {
  name: 'SearchResults',
  template: `
    <div id="search-page-container" class="">
      <div class='controls-container d-flex justify-content-between pt-3'>
        <div id="searchbar-container" class="d-flex">
          <input type="search" v-model='query' id="searchbar" name="searchbar" placeholder="Search" class="form-control align-self-center">
          <label for="searchbar" id='search-btn-label' class="ml-2 align-self-center">
            <img @click='searchTickets' src="/static/assets/search_btn.svg" alt="search icon" id="search-icon" class="">
          </label>
        </div>
      </div>
      <h3 class='mt-3'>
        <b>Search Results</b>
      </h3>
      <table class="table mt-4" id="search-table">
        <caption class="sr-only">Search Results Table</caption>
        <thead>
          <tr>
            <th scope="col">Vehicle Owner</th>
            <th scope="col">Date & Time</th>
            <th scope="col">Offence Desc.</th>
            <th scope="col">Registration #</th>
            <th scope="col">Location</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody v-if='tickets.length > 0' id='search-table-body'>
          <tr v-for='ticket in tickets' @click="viewTicket(ticket.id, ticket.status)">
            <td>{{ticket.vehicleOwner.fname}} {{ticket.vehicleOwner.lname}}</td>
            <td>{{ticket.incident.date}} {{ticket.incident.time}}</td>
            <td>{{ticket.offence.description}}</td>
            <td>{{ticket.vehicle.licenseplate}}</td>
            <td>{{ticket.location.description}}</td>
            <td>{{ticket.status}}</td>
          </tr>
        </tbody>
      </table>
      <div id='search-message' class='d-flex justify-content-center mt-5'>
        <h3 class='mt-3'>
          <span v-if='tickets.length === 0' class='search-count'>No Records Found</span>
          <span v-else-if='tickets.length === 1' class='search-count'>1 Record Found</span>
          <span v-else class='search-count'>{{tickets.length}} Records Found</span>
        </h3>
      </div>
    </div>
    `, data() {
      return {
        tickets: [],
        query: searchQuery
      }
  },
  created() {
    if (isLoggedIn()){
      this.query = searchQuery;
      this.searchTickets();
    }
    else {
      this.$router.push('/login');
    }
  },
  methods: {
    searchTickets() {
      let self = this;
      this.tickets = [];
      fetch(`/api/search/tickets?q=${self.query}`, {
          method: 'GET',
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      })
      .then(function (offenceData) {
        console.log(offenceData);  
        offenceData.forEach((ticket, index) => {
          console.log(ticket);
          self.updateTable(ticket);
        })
      })
      .catch(function (error) {
          console.log(error);
      });
    },
    viewTicket(ticketID,status){
      if(status.search('ISSUED') === 0){
        // IF THE STATUS IS ISSUED ...
        this.$router.push(`/issued/${ticketID}`);
      } else {
        this.$router.push(`/flagged/${ticketID}/${status}`);
      }
    },
    updateTable(offenceData){
      this.tickets.unshift(offenceData);
    }
  }
}

const AccountSettings = {
  name: 'AccountSettings',
  template: `
    <div id="account-page-container" class="">
      <h3 class='mt-3'>
        <b>My Account</b>
      </h3>
      <table class="table mt-4" id="account-table">
        <caption class="sr-only">Change Password Table</caption>
        <thead>
          <tr>
            <th scope="col">Username</th>
            <th scope="col">Password</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody id='account-table-body'>
          <tr>
            <td class='pt-3'>{{user.name}}</td>
            <td id='td-password'>**************</td>
            <td><change-password-btn data-toggle="modal" data-target="#changePasswordModal"></change-password-btn></td>
          </tr>
        </tbody>
      </table>
      <div class="modal fade" tabindex="-1" role="dialog" id="changePasswordModal">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title"><b>CHANGE PASSWORD</b></h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">

              <form method="post" @submit.prevent="changePassword" id="change-password-form" class="d-flex flex-column">
                <input type="hidden" name="userID" id='user-id-field' :value="user.id" required/> 
                <div class="form-group">
                  <label for="oldPassword" class="">Old Password</label>
                  <input type="password" name="oldPassword" class='form-control' id='old-password-field' required/> 
                </div>
                <div class="form-group">
                  <label for="newPassword" class="">New Password</label>
                  <input type="password" name="newPassword" class='form-control' id='new-password-field' required/> 
                </div>
                <div class="modal-footer d-flex justify-content-between px-0">
                  <!--<button v-if='status.search(statusStr) >= 0' type="button" class="btn mt-2 close-btn" data-dismiss="modal">Close</button>-->
                  <button type="submit" name="submit-btn" class="btn save-btn d-flex align-items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#ffffff">
                      <path d="M0 0h24v24H0z" fill="none"/>
                      <path d="M17 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/>
                    </svg>
                  <span>Save changes</span>
                  </button>
                  <transition name="fade" class="mt-3">
                    <div v-if="displayFlash" v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]" class="alert">
                        {{ flashMessage }}
                    </div>
                  </transition>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    `, data() {
      return {
        user: JSON.parse(sessionStorage.getItem('jets_user')),
        status: '',
        statusStr: 'successfully',
        flashMessage: sessionStorage.getItem('flash'),
        displayFlash: false,
        isSuccess: false,
        alertSuccessClass: 'alert-success',
        alertErrorClass: 'alert-danger'
      }
  },
  created() {
    if (!isLoggedIn()){
      this.$router.push('/login');
    }
  },
  methods: {
    changePassword() {
      let self = this;
      //let changePasswordForm = document.getElementById('change-password-form');
      let changePasswordForm = document.forms['change-password-form'];
      let form_data = new FormData(changePasswordForm);
      fetch("/api/users/changePassword", {
          method: 'POST',
          body: form_data,
          headers: {
              'X-CSRFToken': csrf_token,
              'Authorization': 'Bearer ' + sessionStorage.getItem('jets_token')
          },
          credentials: 'same-origin'
      })
      .then(function (response) {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        return response.json();
      })
      .then(function (offenceData) {
        console.log(offenceData)
        self.status = offenceData['message']

        if(self.status.search('successfully') >= 0){
          console.log('Success')
          const oldpswd = document.getElementById('old-password-field');
          oldpswd.value ='';
          const newpswd = document.getElementById('new-password-field');
          newpswd.value ='';
          self.isSuccess = true;
        } else {
          const oldpswd = document.getElementById('old-password-field');
          oldpswd.value ='';
          const newpswd = document.getElementById('new-password-field');
          newpswd.value ='';
        }
        self.displayFlash = true;
        self.flashMessage = self.status;
        setTimeout(function() { 
            self.displayFlash = false;
        }, 3000);
        
      })
      .catch(function (error) {
          console.log(error);
      });
    }
  }
}

const NotFound = {
  name: 'NotFound',
  template: `
  <div class="not-found mt-5">
    <h1>404</h1>
    <p>That page doesn't even exist.</p>
    <p>Why don't you just <router-link to="/">go back notifications</router-link></p>
  </div>

  `,
  data() {
      return {}
  },
  created(){
    if (isLoggedIn()){
      loginNav();
    }
  },
  methods: {
  }
}


/* CREATE APP */
const app = Vue.createApp({
  components: {
    'notifications': Notifications,
    'login': Login
  },
  data() {
    return {
      token: ''
    }
  }
});

/* COMPONENTS */
app.component('app-header', {
  name: 'AppHeader',
  template: `
    <nav id='navbar' class="navbar navbar-expand-lg navbar-dark fixed-top d-flex justify-content-between px-5">
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <router-link to="/flagged">
        <div class="navbar-brand my-0 py-0">
          <div id="website-name" class='d-flex flex-column'>
            <p id='jets' class='mb-0'>JETS</p>
            <p id='jets-long' class='my-0'>JamaicaEye Ticketing System</p>
          </div>
        </div>
      </router-link>
      <div class="collapse navbar-collapse mx-auto" id="navbarSupportedContent">
        <ul id="logged-in" class="navbar-nav w-100">
          <li class="nav-item dynamic-link">
            <router-link class="nav-link" to="/flagged">Notifications</router-link>
          </li>
          <li class="nav-item dynamic-link">
            <router-link class="nav-link" to="/issueTicket">Issue Ticket</router-link>
          </li>
          <li class="nav-item dynamic-link">
            <router-link class="nav-link" to="/issued">Traffic Offenders</router-link>
          </li>
          <li class="nav-item dynamic-link">
            <router-link class="nav-link" to="/archives">Archives</router-link>
          </li>
        </ul>
      </div>
      <ul id="user-menu" class="navbar-nav ml-auto">
        <li class="nav-item dynamic-link dropdown d-inline-block">
          <router-link v-if='userExists' class="nav-link username d-flex justify-content-between" to="">
            <span id='username'>{{user.name}}</span>
            <img src="/static/assets/drop_down_arrow.svg" alt="dropdown arrow" id="dropdown-arrow-icon" class="dropdown-arrow d-inline-block">
          </router-link>
          <div class="dropdown-content rounded">
            <router-link class="nav-link d-flex account-settings rounded-top" to="/accountSettings">
              <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                <g><path d="M0,0h24v24H0V0z" fill="none"/></g>
                <g><g>
                  <path d="M4,18v-0.65c0-0.34,0.16-0.66,0.41-0.81C6.1,15.53,8.03,15,10,15c0.03,0,0.05,0,0.08,0.01c0.1-0.7,0.3-1.37,0.59-1.98 C10.45,13.01,10.23,13,10,13c-2.42,0-4.68,0.67-6.61,1.82C2.51,15.34,2,16.32,2,17.35V20h9.26c-0.42-0.6-0.75-1.28-0.97-2H4z"/>
                  <path d="M10,12c2.21,0,4-1.79,4-4s-1.79-4-4-4C7.79,4,6,5.79,6,8S7.79,12,10,12z M10,6c1.1,0,2,0.9,2,2s-0.9,2-2,2 c-1.1,0-2-0.9-2-2S8.9,6,10,6z"/>
                  <path d="M20.75,16c0-0.22-0.03-0.42-0.06-0.63l1.14-1.01l-1-1.73l-1.45,0.49c-0.32-0.27-0.68-0.48-1.08-0.63L18,11h-2l-0.3,1.49 c-0.4,0.15-0.76,0.36-1.08,0.63l-1.45-0.49l-1,1.73l1.14,1.01c-0.03,0.21-0.06,0.41-0.06,0.63s0.03,0.42,0.06,0.63l-1.14,1.01 l1,1.73l1.45-0.49c0.32,0.27,0.68,0.48,1.08,0.63L16,21h2l0.3-1.49c0.4-0.15,0.76-0.36,1.08-0.63l1.45,0.49l1-1.73l-1.14-1.01 C20.72,16.42,20.75,16.22,20.75,16z M17,18c-1.1,0-2-0.9-2-2s0.9-2,2-2s2,0.9,2,2S18.1,18,17,18z"/>
                </g></g>
              </svg>
              Account Settings
            </router-link>
            <router-link class="nav-link d-flex logout-btn rounded-bottom" to="/logout">
              <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                <g><path d="M0,0h24v24H0V0z" fill="none"/></g>
                <g><path d="M17,8l-1.41,1.41L17.17,11H9v2h8.17l-1.58,1.58L17,16l4-4L17,8z M5,5h7V3H5C3.9,3,3,3.9,3,5v14c0,1.1,0.9,2,2,2h7v-2H5V5z"/></g>
              </svg>
              Logout
            </router-link>
          </div>
        </li>
      </ul>
    </nav>
  `,
  data() {
    return {
      user: JSON.parse(sessionStorage.getItem('jets_user'))
    }
  },
  created(){
    // If no user data exists in session storage
    if(!this.userExists()){
      // Assign default user
      this.user = {'id': -1, 'name':'default'};
    }
  },
  methods: {
    userExists(){
      return sessionStorage.getItem('jets_user') !== null;
    }
  }
  
});

app.component('app-footer', {
    name: 'AppFooter',
    template: 
    `
    <footer id='footer'>
        <div class="navbar navbar-expand-lg navbar-dark fixed-bottom">
          <p class="m-auto">Copyright © 2021 | All Rights Reserved</p>
        </div>
    </footer>
    `,
    data() {
        return {
            // year: (new Date).getFullYear()
        }
    }
});

app.component('search-bar', {
    name: 'SearchBar',
    template: 
    `
      <div id="searchbar-container" class="d-flex">
        <input type="text" v-model='query' id="searchbar" name="searchbar" placeholder="Search" class="form-control align-self-center">
        <label for="fname" id='search-btn-label' class="ml-2 align-self-center">
          <img @click='search' src="/static/assets/search_btn.svg" alt="search icon" id="search-icon" class="">
        </label>
      </div>
    `,
    data() {
        return {
            query: ''
        }
    },
    created(){      
    },
    methods: {
      search(){
        console.log('Searching for ' + this.query)
        if (this.query){
          searchQuery = this.query; // Store globally for access from other components
          this.$router.push('/searchResults');
        }
      }
    }

});

app.component('simulate-btn', {
    name: 'SimulateBtn',
    template: 
    `
     <div class="btn d-flex justify-content-start align-items-center simulate-btn">
        <img src="/static/assets/simulate.svg" alt="Simulate Icon">
        <span class="d-inline-block pl-2">Simulate</span>
      </div>
    `,
    data() {
        return {
        }
    }
});

app.component('issue-btn', {
    name: 'IssueBtn',
    template: 
    `
     <div class="btn d-flex justify-content-start align-items-center issue-btn">
        <img src="/static/assets/issue_ticket.svg" alt="Issue Icon">
        <span class="d-inline-block pl-2">Issue</span>
      </div>
    `,
    data() {
        return {
        }
    }
});

app.component('archive-btn', {
    name: 'ArchiveBtn',
    template: 
    `
     <div class="btn d-flex justify-content-start align-items-center archive-btn">
        <img src="/static/assets/archive.svg" alt="Archive Icon">
        <span class="d-inline-block pl-2">Archive</span>
      </div>
    `,
    data() {
        return {
        }
    }
});

app.component('print-btn', {
    name: 'PrintBtn',
    template: 
    `
     <div class="btn d-flex justify-content-start align-items-center print-btn">
        <img src="/static/assets/print.svg" alt="Print Icon">
        <span class="d-inline-block pl-2">Print</span>
      </div>
    `,
    data() {
        return {
        }
    }
});

app.component('reset-btn', {
    name: 'ResetBtn',
    template: 
    `
     <div class="btn d-flex justify-content-start align-items-center reset-btn">
        <img src="/static/assets/reset.svg" alt="Reset Icon">
        <span class="d-inline-block pl-2">Reset</span>
      </div>
    `,
    data() {
        return {
        }
    }
});

app.component('change-password-btn', {
    name: 'ChangePasswordBtn',
    template: 
    `
     <div id='change-password-btn' class="btn d-flex justify-content-center align-items-center">
        <span class="">Change Password</span>
      </div>
    `,
    data() {
        return {
        }
    }
});

// Define Routes
const routes = [
    { path: "/", component: Notifications },
    { path: "/flagged", component: Notifications },
    // Put other routes here
    { path: '/register', component: Register },
    { path: '/login', component: Login },
    { path: '/logout', component: Logout },
    { path: '/issued', component: Offenders },
    { path: '/issued/:ticketID', component: ViewIssued },
    { path: '/flagged/:ticketID/:ticketStatus', component: ViewFlagged },
    { path: '/archives', component: Notifications },
    { path: '/issueTicket', component: ManualIssue },
    { path: '/searchResults', component: SearchResults },
    { path: '/accountSettings', component: AccountSettings },
    { path: '/accountSettings/admin', component: AccountSettings },

    // This is a catch all route in case none of the above matches
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHistory(),
    routes, // short for `routes: routes`
});

app.use(router);

app.mount('#app');
