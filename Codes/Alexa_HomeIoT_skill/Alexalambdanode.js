/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
 * The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well as
 * testing instructions are located at http://amzn.to/1LzFrj6
 *
 * For additional samples, visit the Alexa Skills Kit Getting Started guide at
 * http://amzn.to/1LGWsLG
 */
var config = {};
const https = require('https');
config.IOT_THING_NAME = "ESP";
var AWS = require('aws-sdk');
AWS.config.region = "eu-west-1";
var iotData = new AWS.IotData({endpoint: "afio7p37diyt8-ats.iot.eu-west-1.amazonaws.com"});

// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.
exports.handler = function (event, context) {
    try {
        console.log("event.session.application.applicationId=" + event.session.application.applicationId);

        /**
         * Uncomment this if statement and populate with your skill's application ID to
         * prevent someone else from configuring a skill that sends requests to this function.
         */
        /*
        if (event.session.application.applicationId !== "amzn1.echo-sdk-ams.app.[unique-value-here]") {
             context.fail("Invalid Application ID");
        }
        */

        if (event.session.new) {
            onSessionStarted({requestId: event.request.requestId}, event.session);
        }

        if (event.request.type === "LaunchRequest") {
            onLaunch(event.request,
                event.session,
                function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === "IntentRequest") {
            onIntent(event.request,
                event.session,
                function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === "SessionEndedRequest") {
            onSessionEnded(event.request, event.session);
            context.succeed();
        }
    } catch (e) {
        context.fail("Exception: " + e);
    }
};

/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
    console.log("onSessionStarted requestId=" + sessionStartedRequest.requestId +
        ", sessionId=" + session.sessionId);
}

/**
 * Called when the user launches the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
    console.log("onLaunch requestId=" + launchRequest.requestId +
        ", sessionId=" + session.sessionId);

    // Dispatch to your skill's launch.
    getWelcomeResponse(callback);
}

/**
 * Called when the user specifies an intent for this skill.
 */
function onIntent(intentRequest, session, callback) {
    console.log("onIntent requestId=" + intentRequest.requestId +
        ", sessionId=" + session.sessionId);

    var intent = intentRequest.intent,
        intentName = intentRequest.intent.name;

    // Dispatch to your skill's intent handlers
    if ("ControlLight" === intentName) {
        setLightInSession(intent, session, callback);
    } else if ("GetProductIntent" === intentName) {
        getproductinfo(intent, session, callback);
    } else if ("AMAZON.HelpIntent" === intentName) {
        getWelcomeResponse(callback);
    } else if ("AMAZON.StopIntent" === intentName || "AMAZON.CancelIntent" === intentName) {
        handleSessionEndRequest(callback);
    } else {
        throw "Invalid intent";
    }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {
    console.log("onSessionEnded requestId=" + sessionEndedRequest.requestId +
        ", sessionId=" + session.sessionId);
    // Add cleanup logic here
}

// --------------- Functions that control the skill's behavior -----------------------

function getWelcomeResponse(callback) {
    // If we wanted to initialize the session to have some attributes we could add those here.
    var sessionAttributes = {};
    var cardTitle = "Welcome";

    'Welcome to Manishs Smart Inventory Management Skill. ' +
        'Would you like to get product types/weights, room temperature or humidity readings?'


    var speechOutput = "Welcome to Manishs Smart Inventory Management Skill. " +
        "Would you like to get product types,weights, room temperature or humidity readings?" + "You also have access to switch on and off the Refrigeration fan";

    // If the user either does not reply to the welcome message or says something that is not
    // understood, they will be prompted again with this text.
    var repromptText = "Please tell me next action";
    var shouldEndSession = false;

    callback(sessionAttributes,
        buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

function handleSessionEndRequest(callback) {
    var cardTitle = "Session Ended";
    var speechOutput = "Thank you for trying Manishs Smart Inventory Management Skill. Have a nice day!";
    // Setting this to true ends the session and exits the skill.
    var shouldEndSession = true;

    callback({}, buildSpeechletResponse(cardTitle, speechOutput, null, shouldEndSession));
}

/**
 * Sets the led in the session and prepares the speech to reply to the user.
 */
function setLightInSession(intent, session, callback) {
    var cardTitle = intent.name;
    var lightStateRequest = intent.slots.LightState;
    var repromptText = "";
    var sessionAttributes = {};
    var shouldEndSession = false;
    var speechOutput = "";

    if (lightStateRequest) {
        var lightState = lightStateRequest.value;
        var paramsUpdate;

        if (lightState === "on") {
            paramsUpdate = {
                "thingName" : config.IOT_THING_NAME,
                "payload" : '{"state" : {"desired" : {"LED" : "ON"}}}'
            };
        } else {
            paramsUpdate = {
                "thingName" : config.IOT_THING_NAME,
                "payload" : '{"state" : {"desired" : {"LED" : "OFF"}}}'
            };
        }

    //Update Device Shadow
    iotData.updateThingShadow(paramsUpdate, function(err, data) {
      if (err){
        console.log(err, err.stack);

        speechOutput = "fail to update thing shadow";
        repromptText = "fail to update thing shadow";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
      }
      else {
        console.log(data);

            sessionAttributes = createLightStateAttributes(lightState);
                speechOutput = "The refrigeration fan has been turned " + lightState;
                repromptText = "The refrigeration fan has been turned" + lightState;
                callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
      }
    });
    } else {
        speechOutput = "Please try again";
        repromptText = "Please try again";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }
}

function createLightStateAttributes(lightState) {
    return {
        lightState: lightState
    };
}



function getproductinfo(intent, session, callback){
    var cardTitle = intent.name;
    var speechOutput = "";
    var repromptText = "";
    var shouldEndSession = false;
    var sessionAttributes = {};
   // const response1 = '{"created_at":"2019-11-25T15:27:00Z","entry_id":2337,"field1":"Horlicks","field2":"20","field3":"58","field4":"3","field5":"77.0","field6":"23.0"}';
   // const response = JSON.parse(response1);

   httpGet().then((data) => {
        const response = data;
           var lightStateRequest = intent.slots.Productinfo.value;
    lightStateRequest = lightStateRequest.toLowerCase();
    var decoded = "";

    if (lightStateRequest==='name'){
        decoded='field1';
        speechOutput = "The " + lightStateRequest + " of the product is " + response[decoded];
        repromptText = "What would you like?";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }

    else if (lightStateRequest==='unit'){
        decoded='field2';
        speechOutput = "The " + lightStateRequest + " weight of the product is " + response[decoded] + " grams" ;
        repromptText = "What would you like?";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));

    }

     else if (lightStateRequest==='total'){
        decoded='field3';
        speechOutput = "The " + lightStateRequest + " weight of the product is " + response[decoded] + " grams";
        repromptText = "What would you like?";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }

    else if (lightStateRequest==='quantity'){
        decoded='field4';
        speechOutput = "The " + lightStateRequest + " of product " + response['field1'] + " is " + response[decoded] + " packets";
        repromptText = "What would you like?";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }

    else if (lightStateRequest==='temperature'){
        decoded='field6';
        speechOutput = "The " + lightStateRequest + " in the warehouse is  " + response[decoded] + " degree celsius ";
        repromptText = "What would you like?";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }

    else if (lightStateRequest==='humidity'){
        decoded='field5';
        speechOutput = "The " + lightStateRequest + " in the warehouse is " + response[decoded] + " percent";
        repromptText = "What would you like?";
        callback(sessionAttributes,buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }

});






}


function httpGet() {
  return new Promise(((resolve, reject) => {
    //var options = {
       // host: 'api.icndb.com',
       // port: 443,
       // path: '/jokes/random',
       // method: 'GET',
    //};

    //const url = 'https://api.thingspeak.com/channels/33251/feed/last.json?api_key=9VGQ4X79MQJC90RD'
    const url = 'https://api.thingspeak.com/channels/913110/feeds/last.json?api_key=FRNOMOXSVMFRVVFF'
    const request = https.get(url, (response) => {
      response.setEncoding('utf8');
      let returnData = '';

      response.on('data', (chunk) => {
        returnData += chunk;
      });

      response.on('end', () => {
        resolve(JSON.parse(returnData));
      });

      response.on('error', (error) => {
        reject(error);
      });
    });
    request.end();
  }));
}



// --------------- Helpers that build all of the responses -----------------------

function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: "PlainText",
            text: output
        },
        card: {
            type: "Simple",
            title: "SessionSpeechlet - " + title,
            content: "SessionSpeechlet - " + output
        },
        reprompt: {
            outputSpeech: {
                type: "PlainText",
                text: repromptText
            }
        },
        shouldEndSession: shouldEndSession
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: "1.0",
        sessionAttributes: sessionAttributes,
        response: speechletResponse
    };
}
