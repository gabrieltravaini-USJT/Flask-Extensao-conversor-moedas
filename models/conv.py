from..extensions import db

class Moeda(db.Model):
    __tablename__ = "Cambio"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preco_compra = db.Column(db.Float)
    preco_venda = db.Column(db.Float)
    data_base = db.Column(db.Date)
    

    def __repr__(self):
        return "<Uc(preco_compra={}, preco_venda={}, data_base={})>".format(self.preco_compra, self.preco_venda, self.data_base)



