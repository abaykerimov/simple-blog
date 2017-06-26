$(document).ready(function () {
    AddComment();
    AddRate();
});

function AddComment() {
    var form = $("#comment_add");
    $(form).submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: $(form).attr('method'),
            url: $(form).attr('action'),
            data: $(form).serialize(),
            success: function (response) {
                if (response.status == 'success') {
                    $(form)[0].reset();
                    $(form).append('<div class="alert alert-success">'+response.message+'</div>');
                    $('.alert').fadeIn(300).delay(1500).fadeOut(400);
                    $('.comments-list').append(
                        '<li class="comment">' +
                        '<a class="pull-left" href="#">' +
                        '<img class="avatar" src="http://bootdey.com/img/Content/user_1.jpg" alt="avatar"> </a> ' +
                        '<div class="comment-body"> <div class="comment-heading"> <h4 class="user">' + response.author +
                        '</h4><h5 class="time">' + response.created +
                        '</h5> </div> <p>' + response.text +
                        '</p> </div> </li>'
                    );
                }
            },
            error: function (response) {
                console.log(response.status);
            }
        });
        $('.alert').remove();
    });
}

function AddRate() {
    var form = $('#article_rate');
    $('.plus-rate').click(function () {
        $.ajax({
            type: $(form).attr('method'),
            url: $(form).attr('action'),
            data: $(form).serialize(),
            success: function (response) {
                if (response.status == 'success') {
                    $('.rate-count').html(response.counts)
                } else {
                    $('.rate-group').append('<span class="warn">'+response.message+'</span>')
                    $('.warn').fadeIn(300).delay(1500).fadeOut(400);
                }
            },
            error: function (response) {
                console.log(response.status);
            }
        });
        $('.warn').remove();
    });
}