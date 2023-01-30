function enableEventBlock( day, month, year) {
    document.getElementById("events").innerHTML = ""
    document.getElementById("Event").style["display"] = "block"
    document.getElementById("date").innerText = day + "." + month + "." + year
    document.getElementById("addEvent").setAttribute("onclick","enableAddEventBlock('"+ day + "." + month + "." + year +"')")
    const formData = new FormData();
formData.append('day', day);
formData.append('month', month);
formData.append('year', year);
    fetch('http://localhost:5000/event', {
  method: 'POST',
  body: formData,
})
  .then(response => response.json())
  .then(data => {
    const eventsContainer = document.getElementById('events');

    data.forEach((eventData) => {
        const title = eventData.title;
        const description = eventData.description;

        const h3 = document.createElement('h3');
        h3.textContent = title.slice(0,20) + "...";;

        const p = document.createElement('p');
        p.textContent = description.slice(0,15) + "...";

        const form = document.createElement("form");
        form.action="/deleteEvent";
        form.method="post";

        const button = document.createElement("button");
        button.textContent = "-";
        button.value = title;
        button.name = "title";
        button.className = "deleteButton";

        eventsContainer.appendChild(h3);
        eventsContainer.appendChild(p);
        form.appendChild(button);
        eventsContainer.appendChild(form);
    });
  })
  .catch(error => console.error('Error:', error));
}

function disableEventBlock() {
    document.getElementById("Event").style["display"] = "none"
}

function enableAddEventBlock(date="Datum DD.MM.JJJJ - DD.MM.JJJJ") {
    document.getElementById("Event").style["display"] = "none";
    document.getElementById("addEventThing").style["display"] = "block";
    document.getElementById("inputDate").value=date;
    document.getElementById("inputTime").value="00:00-23:59";
}
function disableAddEventBlock() {
    document.getElementById("addEventThing").style["display"] = "none"
}