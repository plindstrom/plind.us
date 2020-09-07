/*
  File Name  global.js
  Project    plind.us
  Version    8.1.0
  Author     Peter Lindstrom
  Purpose    Global JS functions utilized throughout the site.
  Copyright  2003-2020, Peter Lindstrom
  Link       https://github.com/plindstrom/plind.us
*/

$(document).ready(function(){
  // Use the preferred theme (light or dark)
  if(localStorage.getItem("theme") === null){
    if(window.matchMedia("(prefers-color-scheme: dark)").matches){
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.setAttribute("data-theme", "light");
    }
  } else {
    document.documentElement.setAttribute("data-theme", localStorage.getItem("theme"));
  }

  // Toggle dark theme on or off
  $(".toggle-theme").click(function(e){
      e.preventDefault();
      if(document.documentElement.getAttribute("data-theme") == "light"){
        localStorage.setItem("theme", "dark");
        document.documentElement.setAttribute("data-theme", "dark");
      } else {
        localStorage.setItem("theme", "light");
        document.documentElement.setAttribute("data-theme", "light");
      }
  });
});