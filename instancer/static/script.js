// left side bar

function openNav() {
    document.getElementById("mySidenav").style.width = "20%";
    // document.getElementById("main").style.marginLeft = "20%";
  }
    
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0%";
    // document.getElementById("main").style.marginLeft = "0%";
  }
  
  
  // search box
  
  const clearInput = () => {
    const input = document.getElementsByTagName("input")[0];
    input.value = "";
  }
    
  const clearBtn = document.getElementById("clear-btn");
  clearBtn.addEventListener("click", clearInput);