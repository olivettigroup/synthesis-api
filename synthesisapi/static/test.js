/*  Controller for the demo page
*   Contains all the eventlisteners and varaibles.
*/
var DemoController = function() {
  
  // Starts all processes
  var init = function() {
    eventListeners();
  }

  var eventListeners = function() {
 
    (function() {
      $("#addParagraph").on("submit", function(e) {
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

        console.log(data)

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
  }

  return {
    init: init
  }
}