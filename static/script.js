document.addEventListener('DOMContentLoaded', function(){
    var coll = document.getElementsByClassName("collapsible");
    var i;
    console.log("DOM content has been loaded.");
    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
    
            // toggle the "active" class on the clicked element (this refers to collapsible element)
            //makes collapsible element visible or not.
            console.log("blob");
            this.classList.toggle("active");
            
        
    
            // next element under the collapsible and set it to the variable content
    
            var content = this.nextElementSibling;

            // check whether the content is currently visible

            if (content.style.display === "block") {
            content.style.display = "none";
            this.textContent = "open bookings"
            
            } else {
            content.style.display = "block";
            this.textContent = "close bookings"
            
            }
        });
    }

})