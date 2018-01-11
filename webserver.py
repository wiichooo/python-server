from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from database_setup import Base, Restaurant, MenuItem 
engine = create_engine('sqlite:///restaurantmenu.db') 
Base.metadata.bind=engine 
DBSession = sessionmaker(bind = engine) 
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		# try:
		# 	if self.path.endswith("/hello"):
		# 		self.send_response(200)
		# 		self.send_header('Content-type', 'text/html')
		# 		self.end_headers()
				
		# 		output = ""
		# 		output += "<html><body>Hello!"
		# 		output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
		# 		output += "</body></html>"
		# 		self.wfile.write(output)
		# 		print output
		# 		return
		
		# except IOError:
		# 	self.send_error(404, "File Not Found %s" & self.path)
		
		# try:
		# 	if self.path.endswith("/hola"):
		# 		self.send_response(200)
		# 		self.send_header('Content-type', 'text/html')
		# 		self.end_headers()
				
		# 		output = ""
		# 		output += "<html><body>Hola!<a href='/hello'>Back to hello</a>"
		# 		output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
		# 		output += "</body></html>"
		# 		self.wfile.write(output)
		# 		print output
		# 		return
		
		# except IOError:
		# 	self.send_error(404, "File Not Found %s" & self.path)
		
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>Hello!"

				items = session.query(Restaurant).all() 
				for item in items: 
					output += "<p>" + item.name + "<br><a href='/restaurants/"+str(item.id)+"/edit'>Edit</a><br><a href='/restaurants/"+str(item.id)+"/delete'>Delete</a></p>"
				
				
				output += "<br><a href='/restaurants/new'>Add</a></body></html>"
				self.wfile.write(output)
				print output
				return
		
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>Add restaurant!"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What would be the name?</h2><input name='restaurant' type='text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
		
			if self.path.endswith("/edit"):

				res = self.path.split("/")[2]
				resQuery = session.query(Restaurant).filter_by(id = res).one()
				if resQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = "<html><body>"
					output += "<h1>"
					output += resQuery.name
					output += "</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % res
					output += "<input name = 'restaurant' type='text' placeholder = '%s' >" % resQuery.name
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</form>"
					output += "</body></html>"

					self.wfile.write(output)
				return
		
			if self.path.endswith("/delete"):
				res = self.path.split("/")[2]
				resQuery = session.query(Restaurant).filter_by(id = res).one()
				if resQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
				
					output = ""
					output += "<html><body>Are you sure you want to delete this restaurant: %s!" % resQuery.name
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input type='submit' value='Submit'></form>" % resQuery.id
					output += "</body></html>"
					self.wfile.write(output)
					
				return
		
		except IOError:
			self.send_error(404, "File Not Found %s" & self.path)
			
	def do_POST(self):
		
		try:
			
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant')
					
				
				newRestaurant = Restaurant(name = messagecontent[0])
				session.add(newRestaurant)
				session.commit()
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant')
					res = self.path.split("/")[2]

					resQuery = session.query(Restaurant).filter_by(
						id=res).one()
					if resQuery != []:
						resQuery.name = messagecontent[0]
						session.add(resQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

			if self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant')
					res = self.path.split("/")[2]

					resQuery = session.query(Restaurant).filter_by(
						id=res).one()
					if resQuery != []:
						session.delete(resQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

		except:
			pass

		# try:
		# 	self.send_response(301)
		# 	self.end_headers()
			
		# 	ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		# 	if ctype == 'multipart/form-data':
		# 		fields = cgi.parse_multipart(self.rfile, pdict)
		# 		messagecontent = fields.get('message')
				
		# 	output = ""
		# 	output += "<html><body>"
		# 	output += "<h2> Okay, how about this: </h2>"
		# 	output += "<h1> %s </h1>" % messagecontent[0]
			
		# 	output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
		# 	output += "</body></html>"
		# 	self.wfile.write(output)
		# 	print output
		# except:
		# 	pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
		
	except KeyboardInterrupt:
		print "ctrl C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()