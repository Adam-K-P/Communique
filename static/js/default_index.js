// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    var aws_base_url = 
       "https://66qgd1ph4a.execute-api.us-east-1.amazonaws.com/prod/";
    var aws_add_post = aws_base_url + "addpost";
    var aws_get_posts = aws_base_url + "getposts";

    Vue.config.silent = false; // show all warnings

    self.add_notf_button = function() {
       self.vue.adding_notf = !self.vue.adding_notf;
    };

    self.get_notfs = function() {
       $.get(get_notfs_url, function(data) {
          self.vue.notifications = data.notifications;
       });
    };

    self.has_phone_number = function() {
       return $.post(has_phone_number_url, {
          user_email: current_user
       });
    };

    self.add_notf = function() {
       $.post(add_notf_url,
          {
             message: self.vue.notf_content,
             user_email: current_user,
             time: self.vue.day_selected +
                   self.vue.hour_selected +
                   self.vue.minute_selected +
                   self.vue.am
          }, function(data) {
             self.vue.notf_content = "";
             self.vue.day_selected = "MON";
             self.vue.hour_selected = "12";
             self.vue.minute_selected = "00";
             self.vue.am = "0";
             self.add_notf_button();
             self.get_notfs();
          });
    };

    self.add_phone_button = function() {
       self.vue.adding_phone_number = !self.vue.adding_phone_number;
    };

    //could use some error checking here
    self.del_notf = function(id) {
       $.post(del_notf_url,
          {
             id_: id
          }, function (data) {
             self.get_notfs();
          }
       );
    };

    self.add_phone_number = function() {
       //should do verification first here
       $.post(add_phone_number_url,
          {
             user_email: current_user,
             phone_number: self.vue.phone_number
          }, function(data) {
             self.vue.phone_number = "";
          });
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
           notifications: [],
           adding_phone_number: false,
           phone_number: "",
           adding_notf: false,
           notf_content: "",
           day_selected: "MON",
           hour_selected: "12",
           minute_selected: "00",
           am: "0",
           days: [ 
             { text: "Monday", value: "MON" },
             { text: "Tuesday", value: "TUE" },
             { text: "Wednesday", value: "WED" },
             { text: "Thursday", value: "THU" },
             { text: "Friday", value: "FRI" },
             { text: "Saturday", value: "SAT" },
             { text: "Sunday", value: "SUN" }
           ],
           hours: [
             { text: "12", value: "12" },
             { text: "1", value: "01" },
             { text: "2", value: "02" },
             { text: "3", value: "03" },
             { text: "4", value: "04" },
             { text: "5", value: "05" },
             { text: "6", value: "06" },
             { text: "7", value: "07" },
             { text: "8", value: "08" },
             { text: "9", value: "09" },
             { text: "10", value: "10" },
             { text: "11", value: "11" }
           ],
           minutes: [
              { text: "00", value: "00" },
              { text: "05", value: "05" },
              { text: "10", value: "10" },
              { text: "15", value: "15" },
              { text: "20", value: "20" },
              { text: "25", value: "25" },
              { text: "30", value: "30" },
              { text: "35", value: "35" },
              { text: "40", value: "40" },
              { text: "45", value: "45" },
              { text: "50", value: "50" },
              { text: "55", value: "55" }
           ],
           meridian: [
              { text: "am", value: "0" },
              { text: "pm", value: "1" }
           ]
        },
        methods: {
           add_notf: self.add_notf,
           add_notf_button: self.add_notf_button,

           del_notf: self.del_notf,

           add_phone_button: self.add_phone_button,

           has_phone_number: self.has_phone_number,

           add_phone_number: self.add_phone_number
        }
    });

    self.get_notfs();
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
