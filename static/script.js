
$(document).ready(function () {
    console.log("ready!")

    $.get("/get_online", function(data, status){
        let users = data;
        $('div#users').html('');

        let area = document.getElementById('users');

        let html_table = `
            <center>
                <h2>Online Users</h2>
            </center>
            <br>
            <table class="table table-hover table-dark ">
            <thead>
                <tr>

                <th scope="col">Name</th>
                <th scope="col">Mac</th>
                <th scope="col">Ip</th>
                <th scope="col">Status</th>
                </tr>
            </thead>
            <tbody>
        `;


        users.forEach(user=>{
            console.log(user);
            html_table += `

            <tr>
                <td>${user.name}</td>
                <td>${user.mac}</td>
                <td>${user.ip}</td>
                <td>
                <label class="switch">
                    <input type="checkbox" id="${user.ip}" onchange=on_off(this) ${(!user.spoofed)?'checked':''}>
                    <span class="slider round"></span>
                </label>
                </td>
            </tr>
            `

        });

        html_table += ` </tbody></table>`;

        area.innerHTML = html_table;



    });

});


function on_off(target) {

    console.log(target.checked  , target.id)


    $.post('spoof', { 'target': target.id, 'type' : (!target.checked)?"spoof":"restore"},
        function(returnedData){
            console.log(returnedData.msg);
        }
    );
}
