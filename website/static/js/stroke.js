function ToggleCheckBox(elem) {
  var TickLine1 = elem.querySelector(".tick>.Tickline1")
  var Tickline2 = elem.querySelector(".tick>.Tickline2")
  if (elem.getAttribute("data-status") == "true") {
      TickLine1.style.opacity = 1
      Tickline2.style.opacity = 1
      elem.setAttribute("data-status", false)

  } else {
      TickLine1.style.opacity = 0
      Tickline2.style.opacity = 0
      elem.setAttribute("data-status", true)


  }
}
