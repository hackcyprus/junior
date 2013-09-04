require.config({
    baseUrl: '/static/javascript/game',
    paths: {
        jquery: [
            '//cdnjs.cloudflare.com/ajax/libs/jquery/1.10.1/jquery.min',
            '../vendor/jquery'
        ],
        underscore: [
            '//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.1/underscore-min',
            '../vendor/underscore'
        ],
        backbone: [
            '//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.0.0/backbone-min',
            '../vendor/backbone'
        ],
        pusher: [
            '//js.pusher.com/2.1/pusher.min',
            '../vendor/pusher'
        ],
        modal: '../vendor/bootstrap-modal'
    },
    shim: {
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        },
        pusher: {
            exports: 'Pusher'
        },
        modal: ['jquery']
    }
});

if (__env__ == 'dev') {
    require.config({
        urlArgs: "bust=" + (new Date()).getTime()
    });
}

require(['jquery', 'modal', 'app'], function($, _, app) {
    app.initialize();
    console.log('initialized');
});