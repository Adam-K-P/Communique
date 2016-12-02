// This is the js for the default/index.html view.

//TODO: error checking on these external requests would be nice

var app = function() {

    var self = {};

    var aws_base_url = 
       "https://66qgd1ph4a.execute-api.us-east-1.amazonaws.com/prod/";
    var aws_add_post = aws_base_url + "addpost";
    var aws_get_posts = aws_base_url + "getposts";

    Vue.config.silent = false; // show all warnings

    //no library function to do this ???
    self.stringify_with_leading_zeros = function(num, size) {
       var num_ = num.toString();
       for (var i = num_.length; i < size; ++i) num_ = "0" + num_;
       return num_;
    };

    self.edit_notf_button = function(id) { //fucking vue...
       for (var i = 0; i < self.vue.editing_notf.length; ++i) {
          if (self.vue.editing_notf[i] == id) { //it's already being edited

             var temp = [];

             for (var j = 0; j < i; ++j)
                temp.push(self.vue.editing_notf[j]);
             for (var j = i + 1; j < self.vue.editing_notf.length; ++j)
                temp.push(self.vue.editing_notf[j]);

             self.vue.editing_notf = temp;

             return;
          }
       }

       self.vue.editing_notf.push(id);
    };

    self.get_edit_time = function(id) {
       var edit_time = self.vue.edit_day_selected[id];
       if (self.vue.edit_meridian_selected[id] == "0")
          edit_time += self.vue.edit_hour_selected[id] == "12" ?
             "00" : self.vue.edit_hour_selected[id];
       else edit_time +=
          self.vue.edit_hour_selected[id] == "12" ?
             "12" : (parseInt(self.vue.edit_hour_selected[id]) + 12).toString();
       return edit_time + self.vue.edit_minute_selected[id];
    }

    self.edit_notf = function(id) {
       $.post(edit_notf_url, {
          notf_id: id,
          message: self.vue.edit_content[id],
          time: self.get_edit_time(id)
       }, function(data) {
          self.edit_notf_button(id);
          self.get_notfs();
       });
    };

    self.is_being_edited = function(id) {
       for (var i = 0; i < self.vue.editing_notf.length; ++i)
          if (self.vue.editing_notf[i] == id)
             return true;
       return false;
    };

    self.add_notf_button = function() {
       self.vue.adding_notf = !self.vue.adding_notf;
    };

    //hour must be passed in as an integer
    self.extract_hour_meridian = function(hour, index) {
       if (hour >= 12) {
          self.vue.edit_meridian_selected[index] = "1";
          self.vue.edit_hour_selected[index] =
             self.stringify_with_leading_zeros(hour == 12 ? 12 : hour - 12, 2);
       } else {
          self.vue.edit_meridian_selected[index] = "0";
          self.vue.edit_hour_selected[index] =
             self.stringify_with_leading_zeros(hour == 0 ? 12 : hour, 2);
       }
    };

    self.get_notfs = function() {

       $.get(get_notfs_url, function(data) {

          self.vue.notifications = data.notifications;

          //may have to consider doing this differently
          for (var i = 0; i < data.notifications.length; ++i) {

             self.vue.edit_day_selected[data.notifications[i].id_] =
                data.notifications[i].time.substring(0, 3);

             self.extract_hour_meridian(
                parseInt(data.notifications[i].time.substring(3, 5)),
                         data.notifications[i].id_);

             self.vue.edit_minute_selected[data.notifications[i].id_] =
                self.stringify_with_leading_zeros
                   (parseInt(data.notifications[i].time.substring(5, 7)), 2);
          }
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
             self.vue.add_phone_button();
          });
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
           notifications: [],

           editing_notf: [],
           edit_content: [],
           edit_day_selected: [],
           edit_hour_selected: [],
           edit_minute_selected: [],
           edit_meridian_selected: [], //0 == am; 1 == pm

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
           edit_notf: self.edit_notf,
           edit_notf_button: self.edit_notf_button,
           is_being_edited: self.is_being_edited,

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
