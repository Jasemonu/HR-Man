$(document).ready(function(){
    $("#hire").datepicker({
      showOn: "button",
      buttonImage: "http://i0.wp.com/advfam.com.br/wp-content/uploads/2016/01/calendario.png",
      buttonImageOnly: true,
      buttonText: "Select date"
    });
  });
  
  function addRecord() {
    var fName = document.getElementById("first_name");
    var lName = document.getElementById("last_name");
    var email = document.getElementById("email");
    var hireDate = document.getElementById("hire");
    var salary = document.getElementById("salary");
    var submit_btn = document.getElementById("submit");
    var table = document.getElementById("employee_table");
    var error_msg = document.getElementById("error_msg");
    var row;
    var cell1;
    var cell2;
    var cell3;
    var cell4;
    var cell5;
    var cell6;
    var cell7;
  
  
    if (fName.value === "") {
      fName.style.backgroundColor = "pink";
      error_msg.innerHTML = "<span style='color:red'> Please enter First Name </span>";
      return;
    }
    if (lName.value === "") {
      lName.style.backgroundColor = "pink";
      error_msg.innerHTML = "<span style='color:red'> Please enter Last name </span>";
      return;
    }
    if (email.value === "") {
      email.style.backgroundColor = "pink";
      error_msg.innerHTML = "<span style='color:red'> Please enter email </span>";
      return;
    }
    if (hireDate.value === "") {
      hireDate.style.backgroundColor = "pink";
      error_msg.innerHTML = "<span style='color:red'> Please enter Hire Date </span>";
      return;
    }
    if (salary.value === "") {
      salary.style.backgroundColor = "pink";
      error_msg.innerHTML = "<span style='color:red'> Please enter salary </span>";
      return;
    }
  
    row = table.insertRow(1);
    cell1 = row.insertCell(0);
    cell2 = row.insertCell(1);
    cell3 = row.insertCell(2);
    cell4 = row.insertCell(3);
    cell5 = row.insertCell(4);
    cell6 = row.insertCell(5);
    cell7 = row.insertCell(6);
    cell1.innerHTML = fName.value;
    cell2.innerHTML = lName.value;
    cell3.innerHTML = email.value;
    cell4.innerHTML = hireDate.value;
    cell5.innerHTML = salary.value;
    cell6.innerHTML = "<input type='button' value='Edit employee' onclick='editRecord(this)'/>";
    cell7.innerHTML = "<input type='button' value='Delete user' onclick='deleteRecord(this)' style='background-color:red' />";
  
  }
  
  function deleteRecord(button) {
    var table = document.getElementById("employee_table");
    var row = button.parentNode.parentNode;
    table.deleteRow(row.rowIndex);
  }
  
  function editRecord(button) {
    var row = button.parentNode.parentNode;
    var td_array = row.children;
    for (i = 0; i < td_array.length - 2; i++) { //the '- 2' is added so the 'edit' and 'delete' buttons won't become editable
      td_array[i].setAttribute("contenteditable", "true");
      td_array[i].style.backgroundColor = "lightblue";
    }
  
    button.parentNode.innerHTML = "<input type='button' style='background-color:lightblue' value='Exit edit mode' onclick='exitRecord(this)'/>";
  }
  
  function exitRecord(button) {
    var row = button.parentNode.parentNode;
  
    var td_array = row.children;
    for (i = 0; i < td_array.length - 2; i++) { //the '- 2' is added so the 'edit' and 'delete' buttons won't be effected
      td_array[i].setAttribute("contenteditable", "false");
      td_array[i].style.backgroundColor = "white";
    }
    button.parentNode.innerHTML = "<input type='button' value='Edit employee' onclick='editRecord(this)'/>"
  
  }
  
  