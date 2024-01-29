// adding Review

const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

$("#commentForm").submit(function (e) {
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log("Comment Saved to....");

            if (response.bool == true) {
                $("#review-res").html("Review added successfully. ")
                $(".hide-comment-form").hide()
                $(".comment-hide").hide()

                let _html = '<div class="course-review-item mb-30">';
                _html += '<div class="course-reviews-img">';
                _html += '<a href="#"><img src="https://img.freepik.com/free-vector/isolated-young-handsome-man-different-poses-white-background-illustration_632498-859.jpg?w=740&t=st=1705036063~exp=1705036663~hmac=7e4aad1057b779c959415ee0590cea2abd067e55a50f070027568a5147b05277" alt="image not found" width="100px"></a>';
                _html += '</div>';

                _html += '<div class="course-review-list">';
                _html += '<h5><a href="#">' + response.context.user + '</a></h5>';
                _html += '<div class="course-start-icon">';

                for (let i = 1; i <= response.context.rating; i++) {
                    _html += '<i class="fas fa-star text-warning"></i>';
                }

                _html += '<span>' + time + '</span>';
                _html += '</div>';

                _html += '<p>' + response.context.review + '</p>';

                _html += '</div>';
                _html += '</div>';

                $(".comment-list").prepend(_html);
            }
        }
    })

})


// Price Range
$(document).ready(function () {

    $(".add-to-cart-btn").on("click", function() {

        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $("#product-quantity-" + index).val()
        let product_name = $(".product-name-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = $("#current-product-price-" + index).text()
        let product_image = $(".product-image-" + index).val()
        

        console.log("Product Quantity:", quantity);
        console.log("Product Name:", product_name);
        console.log("Product ID:", product_id);
        console.log("Product Price:", product_price);
        console.log("Product Image:", product_image);
        console.log("Index:", index);
        console.log("Current Element:", this_val);


        $.ajax({
            url: '/add-to-cart',
            data: {
                'id' : product_id,
                'quantity': quantity,
                'name': product_name,
                'price': product_price,
                'image': product_image,
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding Product to Cart.");
            },
            success: function(response){
                this_val.html("Item added to cart")
                console.log("Added Product to Cart!");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })

    // Delete Items
    $(".delete-product").on("click", function () {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);

        console.log("Product ID:", product_id);


        $.ajax({

            url: "/delete-from-cart/",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Deleting Item...");
                // this_val.hide()
            },
            success: function (response) {
                // this_val.show()
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
                $(".cartdata").load(location.href + ".cartdata");
            },

        });
    });

});


$(document).on("click", ".update-product", function () {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);
    let product_quantity = $(".product-quantity-" + product_id).val()

    console.log("Product ID:", product_id);
    console.log("Product Qty:", product_quantity);

    $.ajax({
        url: "/update-cart",
        data: {
            "id": product_id,
            "quantity": product_quantity,
        },
        dataType: "json",
        beforeSend: function () {
            this_val.addClass('disabled');

            // this_val.hide()
        },
        success: function (response) {

            // this_val.show()
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);
        },

    });
});


// Adding to Wishlist
$(document).on("click", ".add-to-wishlist", function () {
    let product_id = $(this).attr("data-product-item");
    let this_val = $(this);

    console.log("Product ID is:", product_id);

    $.ajax({
        url: "/add-to-wishlist",
        data: {
            'id': product_id
        },
        dataType: 'json',
        beforeSend: function () {
            this_val.html("✔");
            console.log("Added to Wishlist.");
        },
        success: function (response) {
            if (response.bool === true) {
                console.log("Added to Wishlist.");

                // Update wishlist count on the page
                $(".wish-items-count").text(response.wishlist_count);
            }
        }
    });
});


// // Remove from Wishlist
$(document).on('click', '.delete-wishlist-product', function(){
    let wishlist_id = $(this).attr("data-wishlist-product");
    let this_val = $(this);

    console.log("Wishlist is :", wishlist_id);

    $.ajax({
        url: "/remove-from-wishlist/",
        data: {
            "id": wishlist_id,
        },
        dataType: "json",
        type: "GET",
        beforeSend: function() {
            console.log("Deleting product from wishlist.");
        },
        success: function(response){
            if (response.data) {
                $("#wishlist-list").html(response.data);
                // Update wishlist count
                $(".wish-items-count").text(response.wishlist_count);

            } else {
                console.log(response.w);
            }
        },
        error: function(error){
            console.log("Error deleting product from wishlist:", error);
        }
    });
});

// $(document).ready(function () {
//     $("#max_price").on("blur", function () {
//         let min_price = $(this).attr("min");
//         let max_price = $(this).attr("max");
//         let current_price = $(this).val();

//         // console.log("value is:", current_price);
//         // console.log("Max Price is:", max_price);
//         // console.log("Min Price is:", min_price);

//         if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
//             // console.log("Price Error Occured");

//             min_price = Math.round(min_price * 100) / 100
//             max_price = Math.round(max_price * 100) / 100


//             // console.log("Max Price is:", min_price);
//             // console.log("Min Price is:", max_price);

//             alert("Price must between " + min_price + ' and ' + max_price)
//             $(this).val('min_price');
//             $('#range').val(min_price)
//             $(this).focus()

//             return false
//         }
//     });
// });

// $(document).ready(function () {
//     $('#price-filter-btn').on('click', function () {
//         let filter_object = {};

//         let min_price = $("#min_price").val(); // Assuming you have an input with id 'min_price'
//         let max_price = $("#max_price").val();

//         filter_object.min_price = min_price;
//         filter_object.max_price = max_price;

//         $.ajax({
//             url: '/filter-product',
//             data: filter_object,
//             dataType: 'json',
//             beforeSend: function () {
//                 console.log('Sending Data');
//             },
//             success: function (response) {
//                 console.log(response);
//                 $("#filtered-product").html(response.data);
//             }
//         });
//     });
// });




