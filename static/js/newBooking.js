const dateSelector = document.getElementById("newbooking-date")

if (dateSelector) {
    const points = parseInt(document.getElementById("newbooking-newpoints").value)
    const nights = parseInt(document.getElementById("newbooking-newnights").value)
    const startdate = document.getElementById("newbooking-startdate")
    const enddate = document.getElementById("newbooking-enddate")
    startdate.value = new Date().toISOString().split("T")[0]
    enddate.value = new Date().toISOString().split("T")[0]
    console.log("Date picker detected")
    $("#newbooking-date").daterangepicker({
        locale: { format: "DD/MM/YYYY" },
        maxSpan: { days: 14 },
        cancelButtonClasses: "btn-light",
        minDate: new Date(),
    }, function(start, end) {
        let newNights = Math.floor((end - start) / (1000 * 60 * 60 * 24))
        console.log(`New selection: ${start.format('YYYY-MM-DD')} to ${end.format('YYYY-MM-DD')} (${newNights} nights)`)
        startdate.value = start.format('YYYY-MM-DD')
        enddate.value = end.format('YYYY-MM-DD')
        document.getElementById("newbooking-nights").value = newNights
        let multiplier = document.getElementById("newbooking-multiplier").value
        let newPoints = newNights * multiplier
        document.getElementById("newbooking-points").value = newPoints
        document.getElementById("newbooking-newnights").value = nights +  newNights
        document.getElementById("newbooking-newpoints").value = points +  newPoints
        const newMembership = document.getElementById("newbooking-newmembership")
        if (nights +  newNights >= 100) {
            newMembership.innerHTML = "<span class=\"badge badge-platinum rounded-pill d-inline\">Platinum</span>"
        } else if (nights +  newNights >= 30) {
            newMembership.innerHTML = "<span class=\"badge badge-gold rounded-pill d-inline\">Gold</span>"
        } else {
            newMembership.innerHTML = "<span class=\"badge badge-silver rounded-pill d-inline\">Silver</span>"
        }
    });
}
