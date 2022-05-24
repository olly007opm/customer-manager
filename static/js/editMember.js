function editMember(member) {
    resetEditMember()
    document.getElementById("editmember-cover").hidden = true
    document.getElementById("editmember-id").value = member.id
    document.getElementById("editmember-memberId").value = member.memberId
    document.getElementById("editmember-surname").value = member.surname
    document.getElementById("editmember-joined").value = member.joined
    document.getElementById("editmember-nights").value = member.nights
    document.getElementById("editmember-points").value = member.points

    switch (member.membership) {
        case "Silver": {
            document.getElementById("editmember-membership1").checked = true
            break
        }
        case "Gold": {
            document.getElementById("editmember-membership2").checked = true
            break
        }
        case "Platinum": {
            document.getElementById("editmember-membership3").checked = true
            break
        }
    }
}

function resetEditMember() {
    document.getElementById("editmember-cover").hidden = false
    document.getElementById("editmember-id").value = null
    document.getElementById("editmember-memberId").value = null
    document.getElementById("editmember-surname").value = null
    document.getElementById("editmember-joined").value = null
    document.getElementById("editmember-nights").value = null
    document.getElementById("editmember-points").value = null
    document.getElementById("editmember-membership1").checked = false
    document.getElementById("editmember-membership2").checked = false
    document.getElementById("editmember-membership3").checked = false
}