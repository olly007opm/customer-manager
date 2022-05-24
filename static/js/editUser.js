function editUser(user) {
    resetEditUser()
    console.log(user)
    document.getElementById("edituser-cover").hidden = true
    document.getElementById("edituser-id").value = user.id
    document.getElementById("edituser-name").value = user.name
    document.getElementById("edituser-email").value = user.email


    document.getElementById("edituser-admin").checked = user.admin === "True"
    document.getElementById("edituser-admin").disabled = user.id === 1
}

function resetEditUser() {
    document.getElementById("edituser-cover").hidden = false
    document.getElementById("edituser-id").value = null
    document.getElementById("edituser-name").value = null
    document.getElementById("edituser-email").value = null
    document.getElementById("edituser-password").value = null
    document.getElementById("edituser-admin").checked = false
}