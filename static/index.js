var center= function(refEl, el){
            var $window = refEl;
            var top = ($window.height() - el.height() ) /2;
            var left = ($window.width() - el.width() ) / 2;
            el.css( {
                  'top': ( top + $window.scrollTop() )/2,
                  'left': left  + $window.scrollLeft(),
                        } );
      };


upcSubmission = {};
( function( exportObj ){
      exportObj.submitUPC = function(){
            // grabs text inside input box 
            // resets input box
            // removes price container if already exists from last query
            // makes an AJAX call
            // execute callback once server responds with price
            var upc = $('#upc-input').val();
            $('#upc-input').val('');

            $.ajax( { url: '/get_price/'+upc,
                  type: 'GET',
                  dataType: 'json',
                  success: ajaxComplete
            } );

      }

      ajaxComplete = function(response){
            // removes ajax loading element
            // edits price element's price
            if ($('#loading').length >= 1){
                  $('#loading').remove();
            }
            productInfo = response;
            if (productInfo['price'] != 'None'){
                  var priceEl = $('<div id="price">'+productInfo['price']+'</div>');
                  var url = 'http://amazon.com/gp/product/' + productInfo['asin'];
                  var infoEl = $('<div id="info"> <a href="'+ url +'" target="_blank"> Amazon Product Page </a></div>');
            }
            else{
                  var priceEl = $('<div id="price">Price scrape: unsuccesful.</div>');
                  var infoEl = $('<div id="info">Either the product does not exist on Amazon, or Amazon blocked the scrape.</div>');
            }
            
            $('#price').replaceWith(priceEl);
            $('#info').replaceWith(infoEl);
      }

      exportObj.ajaxLoading = function(){
            // creates loading element
            // appends to page
            var loadingDiv = $('<div id="loading" style="z-index: 1000;"> <img src="static/loading.gif" alt="loading price" height="100" width="100"></div>');
            $('#container').append(loadingDiv);
      }

} ) (upcSubmission);


