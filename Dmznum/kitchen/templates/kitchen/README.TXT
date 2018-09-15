THOMPSON...
the base is ready for the kitchen...

BUT...
when i use it in the ADD page, the dropdown no longer works
if you open that page in your browser and inspect it, you'll see something like this

<select name="course_name" required="" id="id_course_name" class="browser-default">
  <option value="" selected="">---------</option>

  <option value="1">CSIT 102:INTRO. TO PROGRAMMING</option>

</select>
........................
that class="browser-default" isn't there by default, but if you add it in your browser inspect window, you realise that the drop down is now showing
so how do we make it add by default??