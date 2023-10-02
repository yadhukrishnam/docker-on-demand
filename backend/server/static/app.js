const get_images = async () => {
    $.ajax({
        type: 'GET',
        dataType: "json",
        url: '/api/get_images',
        headers: {
            'Content-Type': 'application/json'
        },
        success: function (data, status, xhr) {
            for (image in data.images) {
                $("#imagestable").find('tbody')
                    .append($('<tr>')
                        .append($('<td>')
                        .text(image)
                        )
                        .append($('<td>')
                        .text(data.images[image].imagename)
                        )
                        .append($("<td>")
                        .text(data.images[image].port)
                        )
                        .append($("<td>")
                            .append($("<a>")
                                .attr("data-image", data.images[image].imagename)
                                .attr("data-feather", "play")
                                .text("Deploy")
                                .attr("onclick", `deploy_image(this);`)
                            )
                        )
                    );
            }
            feather.replace(); 
        }
    });
}

const deploy_image = async (obj) => {
    let data = {
        "user_id": "admin",
        "image_id": $(obj).attr("data-image")
    };

    $.ajax({
        type: 'POST',
        dataType: "json",
        url: '/api/deploy',
        data: JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json'
        },
        success: function(data, status, xhr) {
            alert(`Deployed ${$(obj).attr("data-image")} successfully.`)
        }
    }); 
}

const active_deployments = async () => {
    $.ajax({
        type: 'POST',
        dataType: "json",
        url: '/api/get_deployments',
        headers: {
            'Content-Type': 'application/json'
        },
        success: function (data, status, xhr) {
            let count = 0; 
                
            for (deployment in data.deployments) {
                $("#deploymentstable").find('tbody')
                    .append($('<tr>')
                        .append($('<td>')
                        .text(count++)
                        )
                        .append($('<td>')
                        .text(deployment)
                        )
                        .append($('<td>')
                        .text(data.deployments[deployment].user_id)
                        )
                        .append($('<td>')
                        .text(data.deployments[deployment].port)
                        )
                        .append($('<td>')
                        .text(new Date(data.deployments[deployment].created_at).toISOString())
                        )
                        .append($("<td>")
                            .append($("<a>")
                                .attr("data-image", deployment)
                                .attr("data-feather", "stop-circle")
                                .text("Kill")
                                .attr("onclick", `kill_deployment(this);`)
                            )
                        )
                    );
            }
            feather.replace(); 
        }
    });
}

const kill_deployment = async (obj) => {
    let data = {
        "user_id": "admin",
        "image_id": $(obj).attr("data-image")
    };

    $.ajax({
        type: 'POST',
        dataType: "json",
        url: '/api/kill',
        data: JSON.stringify(data), 
        headers: {
            'Content-Type': 'application/json'
        },
        success: function(data, status, xhr) {
            alert(`Killed ${$(obj).attr("data-image")} successfully.`);
            $(obj).parent().parent().remove();
        }
    }); 
}