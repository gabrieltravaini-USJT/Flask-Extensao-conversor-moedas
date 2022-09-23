from..extensions import db

class Moeda(db.Model):
    __tablename__ = "Cambio"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    tipo = db.Column(db.String(50))
    inicio = db.Column(db.Date)
    fim = db.Column(db.Date)

    def __repr__(self):
        return "<Uc(nome={}, tipo={}, inicio={}, fim={})>".format(self.nome, self.tipo, self.inicio, self.fim)
    