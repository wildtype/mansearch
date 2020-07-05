require 'nokogiri'
require 'sqlite3'

db = SQLite3::Database.new('man.db')
db.execute 'CREATE VIRTUAL TABLE IF NOT EXISTS manpages_fts USING fts4(page, description, content)'

manpages = %x(man -k .).split("\n")

manpages.map do |manpage|
  page_section, description = manpage.split(/\s+\-\s+/)
  page, _section = page_section.split(' ')
  content = Nokogiri::HTML(
    %x(man -Thtml #{page})
  ).css('body').text

  db.execute(
    'INSERT INTO manpages_fts (page, description, content) VALUES(?,?,?)',
    page, description, content
  )
end

db.close
