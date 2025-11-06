from typing import Optional
from re import fullmatch
from abc import ABC, abstractmethod
 
class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float):
        if not isinstance(name, str) or not bool(fullmatch(r'[A-Za-z]+[0-9]+', name)):
            raise ValueError("Nazwa produktu jest niepoprawna")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Cena produktu jest niepoprawna")
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price
 
    def __hash__(self):
        return hash((self.name, self.price))
 
 
class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass
 
 
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


class Server(ABC):
    n_max_returned_entries = 3
    @abstractmethod
    def get_entries(self, n_letters):
        pass


class ListServer(Server):
    def __init__(self, products: list[Product], n_max_returned_entries_ = 3):
        if not isinstance(products, list) or all(isinstance(p, Product) for p in products):
            raise ValueError("Products powinny być listą obiektów typu Product")
        if n_max_returned_entries_ not in range(3,8):
            raise ValueError("max_returned musi być z przedzialu 3 - 7")
        
        self.products = products
        self.n_max_returned_entries = n_max_returned_entries_
    
    def get_entries(self, n_letters: int = 1) -> list[Product]:
        wyszukane = []
        for product in self.products:
            letter_count = sum(c.isalpha() for c in product.name)
            number_count = sum(c.isdigit() for c in product.name)
            if letter_count == n_letters and (number_count == 2 or number_count == 3):        
                wyszukane.append(product)
            if len(wyszukane) > self.n_max_returned_entries:
                raise TooManyProductsFoundError()
        return sorted(wyszukane, key=lambda p: p.price)
    

class MapServer(Server):
    def __init__(self, products: list[Product], n_max_returned_entries_ = 3):
        if not isinstance(products, list) or all(isinstance(p, Product) for p in products):
            raise ValueError("Products powinny być listą obiektów typu Product")
        if n_max_returned_entries_ not in range(3,8):
            raise ValueError("max_returned musi być z przedzialu 3 - 7")
        
        self.products = {product.name: product for product in products}
        self.n_max_returned_entries = n_max_returned_entries_

    def get_entries(self, n_letters: int = 1) -> list[Product]:
        wyszukane = []
        for product in self.products.values():
            letter_count = sum(c.isalpha() for c in product.name)
            number_count = sum(c.isdigit() for c in product.name)
            if letter_count == n_letters and (number_count == 2 or number_count == 3):        
                wyszukane.append(product)
            if len(wyszukane) > self.n_max_returned_entries:
                raise TooManyProductsFoundError()
        return sorted(wyszukane, key=lambda p: p.price)
 
 
class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server):
        if not isinstance(server, Server):
            raise ValueError('Argumentem powinien być serwer')
        self.server = server
 
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try: 
            wyszukane = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        if not wyszukane:
            return None
        Total_price = sum(p.price for p in wyszukane)
        return Total_price