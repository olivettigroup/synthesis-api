/*  Controller for the demo page
*   Contains all the eventlisteners and varaibles.
*/
var DemoController = function() {
  
  // Starts all processes
  var init = function() {
    eventListeners();
  }

  var eventListeners = function() {
 
    // ======================== UPDATING PARAGRAPH
    (function() {
      $("#updateParagraph").on("submit", function(e) {
        e.preventDefault();

        material_id = $(this)[0].elements["material_id"].value;
        doi = $(this)[0].elements["doi"].value
        text = $(this)[0].elements["text"].value
        is_recipe = $(this)[0].elements["is_recipe"].value == '1'
        update_type = $(this)[0].elements["update_type"].value

        var data = {
          'update_type': update_type,
          'material_id': material_id,
          'rank': 1,
          'paragraph_text': text,
          'doi': doi,
          'is_recipe': is_recipe,
          'feature_vector': '1,2,3'
        };  

        $.ajax({
          datatype: 'json',
          type: 'POST',
          url: '/update_paragraphs',
          data: data
        }).always(function(res){
          $("#addParagraphResponse").text(JSON.stringify(res));
        });
        // alert(data['is_recipe']);
      }); 
    })();

    // ======================== RECORDING MPID FEEDBACK
    (function() {
      $("#mpidFeedback").on("submit", function(e) {
        e.preventDefault();

        var data = {
          'user_id': $(this)[0].elements["user_id"].value,
          'paragraph_id': $(this)[0].elements["paragraph_id"].value,
          'material_id': $(this)[0].elements["material_id"].value,
          'value': $(this)[0].elements["value"].value
        };  

        $.ajax({
          datatype: 'json',
          type: 'POST',
          url: '/record_is_related_feedback',
          data: data
        }).always(function(res){
          $("#mpidFeedbackResponse").text(JSON.stringify(res));
        });
      }); 
    })();

    // ======================== RECORDING IS RECIPE FEEDBACK
    (function() {
      $("#isRecipeFeedback").on("submit", function(e) {
        e.preventDefault();

        var data = {
          'user_id': $(this)[0].elements["user_id"].value,
          'paragraph_id': $(this)[0].elements["paragraph_id"].value,
          'material_id': $(this)[0].elements["material_id"].value,
          'value': $(this)[0].elements["value"].value
        };  

        $.ajax({
          datatype: 'json',
          type: 'POST',
          url: '/record_is_recipe_feedback',
          data: data
        }).always(function(res){
          $("#isRecipeFeedbackResponse").text(JSON.stringify(res));
        });
      }); 
    })();


  }

  return {
    init: init
  }
}