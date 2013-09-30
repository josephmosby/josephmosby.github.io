ISText.SMS = DS.Model.extend({
	account_sid = DS.attr('string'),
	body = DS.attr('string'),
	date_created = DS.attr('string'),
	date_sent = DS.attr('string'),
	from = DS.attr('string'),
});

ISText.Idea = DS.Model.extend({
	
});