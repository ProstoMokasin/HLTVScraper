const validator = require('validator')
const chalk = require('chalk')
const yargs = require('yargs')

yargs.version('1.1.0')

//adding a note
yargs.command({
	command: 'add',
	describe: 'Add a new note',
	handler: function ( ) {
		console.log('adding a new note')
	}
})

//removing a note
yargs.command({
	command: 'remove',
	describe: 'remove a note',
	handler: function ( ) {
		console.log('removing the note')
	}
})

//listing a note
yargs.command({
	command: 'list',
	describe: 'list a note',
	handler: function () {
		console.log('listing the note')
	}
})

yargs.command({
	command: 'read',
	describe: 'read a note',
	handler: function () {
		console.log('reading the note')
	}
})

console.log(yargs.argv)