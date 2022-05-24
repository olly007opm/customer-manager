const surname = document.getElementById("addmember-surname")
const yearJoined = document.getElementById("addmember-joined")

if (surname && yearJoined) {
    function updateMemberId() {
        let formattedSurname = surname.value.charAt(0).toUpperCase() + surname.value.substring(1, 3)
        memberId.value = formattedSurname + randomnum + yearJoined.value.toString().substring(2)
    }
    const randomnum = document.getElementById("addmember-memberId").value
    const memberId = document.getElementById("addmember-memberId")
    memberId.value = randomnum + yearJoined.value.toString().substring(2)
    surname.addEventListener('change', (event) => {
        console.log(`Surname ${event.target.value}`)
        surname.value = surname.value.charAt(0).toUpperCase() + surname.value.slice(1)
        updateMemberId()
    })

    yearJoined.addEventListener('change', (event) => {
        console.log(`year ${event.target.value}`)
        updateMemberId()
    })
}
