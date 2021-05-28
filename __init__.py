from flask import render_template,session,jsonify,json,request
from CTFd.plugins import register_plugin_assets_directory
from CTFd.models import db
from CTFd.plugins.challenges import BaseChallenge
from CTFd.plugins.CTFDolphine.DockDolphine import run_image,stop_image,check_dolphine_service
from CTFd.api.v1.helpers.request import validate_args
from CTFd.utils.decorators import authed_only,admins_only
from CTFd.utils.user import get_current_user


def create_ctfdolphine_challenge(args):
	par = json.loads(args)
	challenge = BaseChallenge.challenge_model(**par)
	db.session.add(challenge)
	db.session.commit()

	return

def load(app):
	register_plugin_assets_directory(app, base_path='/plugins/CTFDolphine/assets/')
	@app.route('/admin/ctfdolphine', methods=['GET'])
	@admins_only
	def ctfdolphine_index():
		return render_template('page.html', content=render_template('plugins/CTFDolphine/assets/index.html'))

	@app.route('/admin/ctfdolphine/create',methods=['GET'])
	@admins_only
	def ctfdolphine_create():
		if request.method == 'GET':
			if request.args.get("arg"):
				create_ctfdolphine_challenge(request.args.get("arg"))
				return jsonify(['1'])
				
			return render_template('plugins/CTFDolphine/assets/create.html') 		
			

	@app.route('/ctfdolphine/run/<image>',methods=['GET'])
	@authed_only
	def ctfdolphine_run_image(image):
		if not check_dolphine_service():
			return jsonify(['Run image error ,service not on']);
		if session.get('ctfdolphine'):
			stop_image(session.get('ctfdolphine')[0])
			session.pop('ctfdolphine')

		session['ctfdolphine'] = run_image(image)
		return jsonify(session['ctfdolphine'][1:])


	@app.route('/ctfdolphine/stop',methods=['GET']) 
	@authed_only
	def ctfdolphine_stop_image():
		if session.get('ctfdolphine'):
			stop_image(session.get('ctfdolphine')[0])
			session.pop('ctfdolphine')
		return jsonify(['1'])

	@app.route('/ctfdolphine/stats',methods=['GET']) 
	@authed_only
	def ctfdolphine_stats():
		if session.get('ctfdolphine'):
			return jsonify(['1'])
		else:
			return jsonify(['0'])

	
