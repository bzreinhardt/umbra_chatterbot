

var fakeServer = function(address) {
  this.address = address;
};

fakeServer.prototype.sendMessage = function(message) {
  console.log('sending message to server: ' + message);
};

// UiBot 
var UiBot = function(user) {
  this.exercise_log = [];
  this.mood_log = [];
  this.exercises = ["squat", "pushup", "run", "deadlift"];
  this.moods = ["happy", "sad", "excited", "worried", "tired"];
  this.parsers = [];
  // map between information and whether it needs to be answered
  this.unanswered_questions = [];
  this.answered_questions = [];
  this.answers = [];

};

UiBot.prototype.AddQuesion = function(question) {
  this.unanswered_questions.push(question);
}

UiBot.prototype.AnswerQuestion = function(question, answer) {
  question_index = -1;
  question_found = false;
  while (!question_found) {
    question_index++;
    if (0 == question.localeCompare(this.unanswered_questions[question_index])) {
      question_found = true;
    }
  }
  this.unanswered_questions.splice(question_index, 1);
  this.answered_questions.push(question);
  this.answers.push(answer);
}


UiBot.prototype.ExercisePush = function(response) {
  for (i = 0; i < this.exercises.length; i++) {
    if (response.indexOf(this.exercises[i]) != -1) {
      this.exercise_log.push(response);
      console.log('logging exercise');
    }
  }
};

UiBot.prototype.MoodPush = function(response) {
for (i = 0; i < this.moods.length; i++) {
    if (response.indexOf(this.moods[i]) != -1) {
      this.mood_log.push(response);
      console.log('logging mood');
    }
  }
};

UiBot.prototype.TellAll = function() {
  /*
  response = "moods are: \n";
  for (i = 0; i < this.mood_log.length; i++) {
    response = response + this.mood_log[i] + " \n";
  }
  response += "exercises are: \n"
  for (i = 0; i < this.exercise_log.length; i++) {
    response = response + this.exercise_log[i] + " \n";
  }
  */
  for (i = 0; i < this.parsers.length; i++) {
    response += this.parsers[i].Print();
  }
  return response;
};

UiBot.prototype.AddParser = function(type) {
  console.log("type is " + type);
  var parser = new Parser(type);
  parser.type = type;
  //check to make sure parser doesn't exist
  already_exists = false;
  parser_index = -1;
  for (i = 0; i < this.parsers.length; i++) {
    if (type.indexOf(this.parsers[i].type) != -1) {
      already_exists = true;
      parser_index = i;
      console.log("parser exists");
    }
  }
  if (!already_exists) {
    this.parsers.push(parser);

    parser_index = this.parsers.length - 1;
    console.log("parser index = " + parser_index);
    console.log("adding new parser = " + parser.type);
    console.log("adding new parser = " + this.parsers[parser_index].type);
  }
  console.log("parser index = " + parser_index);
  return parser_index;
}

// Do all necessary logic on input text
UiBot.prototype.Parse = function(input) {
  response = "";
  // Do parsing
  this.ExercisePush(input);
  this.MoodPush(input);
  for (i = 0; i < this.parsers.length; i++) {
    this.parsers[i].Parse(input);
  }
  if (input.indexOf("parser:") != -1) {
    console.log("parser index = " + input.indexOf("parser:"));
    console.log(input);
    console.log ("type should be: " + input.substring(input.indexOf("parser:") + 7, input.length));
    parser_index = this.AddParser(
                      input.substring(input.indexOf("parser:") + 7, input.length));
    if (input.indexOf("category:") != -1) {
      this.parsers[parser_index].AddCategory(
        input[input.indexOf("category:") + 9, input.length]);
    }
  }
  // generate responses
  if (input.indexOf("data") != -1) {
    response = this.TellAll();
  } else {
    response = "well that's intriguing";
  }
  return response;
}

// 
var Parser = function(type) {

  // Area of interest, like "exercise"
  this.type = type;
  console.log("add parser of type: " + this.type);
  // categories of the type - essentially trigger words
  this.categories = [];
  // Log entries related to the categories
  this.category_log = [];

};

// Add a relevant response to ths parser's logs
Parser.prototype.Parse = function(thing) {
  for (i = 0; i < this.categories.length; i++) {
    // add to the log if one of the categories exists in the statement
    if (thing.indexOf(this.categories[i]) != -1) {
      this.category_log.push(thing);
      console.log("logging " + this.type);
    }
  }
};

// print all the logs this parser consumed
Parser.prototype.Print = function() {
  //TODO(breinhardt) should have pluralization
  response = "type: " + this.type + " categories: ";
  for (i = 0; i < this.categories.length; i++) {
    response += this.categories[i] + " ";
  }
  response += "category logs: "
  for (i = 0; i < this.category_log.length; i++) {
    response += this.category_log[i] + " ";
  }
  return response;
};

var csrftoken = Cookies.get('csrftoken');
console.log('bot url ' + chatterbotUrl);

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});




        

// Called on a new input to the box
function NgChatCtrl($scope, $timeout) {
    // Our server to connect to
    var fake_server = new fakeServer('http://127.0.0.1:8002')
    var side = 'left';
    var ui_bot = new UiBot("Ben");
    // Messages, client info & sending
    $scope.messages = [];

    function submitInput(input) {
      var inputData = {
        'text': input
      }

      var $submit = $.ajax({
        type: "POST",
        url: chatterbotUrl,
        data: inputData,
      });
      var response;
      $submit.done(function(statement) {
        console.log("response is " + statement.text);
                 
        if (statement.text.localeCompare("") != 0) {
          console.log("pushing response");
          $scope.messages.push({
            text: statement.text,
            side: side
          })
        }
          // flip the side
        side = side == 'left' ? 'right' : 'left';
        $scope.messageText = "";
        $scope.$apply();

      
        $("#viewport-content").animate({
            bottom: $("#viewport-content").height() - $("#viewport").height()
        }, 100);

      
      });

      $submit.fail(function() {
        // TODO: Handle errors
      });
    }   
            
    $scope.sendMessage = function () {
        console.log('sending message: ' + $scope.messageText);
        fake_server.sendMessage($scope.messageText);
        response = submitInput($scope.messageText);
        console.log("response = " + response);
        // response = ui_bot.Parse($scope.messageText);
        //if (ui_bot.unanswered_questions.length > 0) {
        //  $scope.messages.push({
        //    //avatar: "data:image/png;base64," + 0,
        //  text: ui_bot.unanswered_questions[0],
        //  side: side
        //});
        //}
        //print what the person wrote to the screen no matter what
        
          $scope.messages.push({
              //avatar: "data:image/png;base64," + 0,
            text: $scope.messageText,
            side: side
          });
      
        //
        // flip the side
        side = side == 'left' ? 'right' : 'left';
        $scope.messageText = "";
        // TODO(breinhardt) scope.apply causes errors but also 
        // seems like the only way to get the message to push
        // $scope.$apply();
        
        $("#viewport-content").animate({
            bottom: $("#viewport-content").height() - $("#viewport").height()
        }, 100);


        

        

        // check whether the response is null in order to print
 
        
    };


    // behavior script
    // List adding question: what do you want to improve?
    // A: exercise - add exercise to a list of things to keep track of
    // List augmenting question: what sort of exercise do you do?
    // A: get execise names and slide into dumb forms - add all to list



    // Occurs when we receive chat messages
    /*
    server.on('ngChatMessagesInform', function (p) {
        $scope.messages.push({
            avatar: "data:image/png;base64," + p.avatar.toBase64(),
            text: p.message,
            side: side
        });
        $scope.$apply();

        // Animate
        $("#viewport-content").animate({
            bottom: $("#viewport-content").height() - $("#viewport").height()
        }, 250);

        // flip the side
        side = side == 'left' ? 'right' : 'left';
    });

    // Once connected, we need to join the chat
    server.on('connect', function () {
        server.joinNgChat();
    });
*/
}