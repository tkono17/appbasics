from enum import Enum
from pydantic import BaseModel
import logging

log = logging.getLogger(__name__)

class QueryOperator(Enum):
    EQ = '='
    NEQ = '!='
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    CONTAINS = 'CONTAINS'
    
QOp = QueryOperator

class QueryLogic(Enum):
    AND = '&'
    OR = '|'
    NOT = '!'

QL = QueryLogic

class QueryCondition(BaseModel):
    name: str | None = None

    def passed(self, data):
        x = False
        return x

class SimpleQuery(QueryCondition):
    op: QueryOperator
    fieldName: str
    value: int | float | str

    def passed(self, data):
        x = False
        actualValue = None
        if self.fieldName in data:
            actualValue = data[self.fieldName]
        else:
            return x
        match self.op:
            case QOp.EQ: x = actualValue == self.value
            case QOp.NEQ: x = actualValue != self.value
            case QOp.GT: x = actualValue > self.value
            case QOp.GE: x = actualValue >= self.value
            case QOp.LT: x = actualValue < self.value
            case QOp.LE: x = actualValue <= self.value
            case QOp.CONTAINS:
                x = actualValue.lower().contains(self.value.lower())>=0
        return x
    
    def where(self):
        value = f'{self.value}'
        if self.op == QOp.CONTAINS or type(self.value) == str:
            value = f'"{self.value}"'
        expr = f'{self.fieldName}{self.op}{value}'
        return expr

class CompositeQuery(QueryCondition):
    logic: QueryLogic | None = None
    conditions: list[QueryCondition] | None = None

    def passed(self, data):
        y = False
        results = [ cond.passed(data) for cond in self.conditions ]
        n = len(self.conditions)
        match self.logic:
            case QL.NOT:
                if n==1: y = not results[0]
            case QL.AND:
                if results.count(True)==n: y = True
            case QL.NOT:
                if results.count(True)>0: y = True
        return y
    
    def where(self):
        expr = ''
        ncond = len(self.conditions)
        if self.logic == QL.NOT:
            if ncond==1:
                expr = f'NOT ({self.conditions[0].where()})'
            else:
                log.warning(f'  Exactly one condition is expected for NOT ({ncond} given)')
        else:
            for cond in self.conditions:
                if len(expr) == 0:
                    expr = cond.where()
                expr += str(self.logic) + cond.where()
        return expr


class QCgen:
    @classmethod
    def condition(cls, name, op, key, value):
        return SimpleQuery(name=name, op=op, fieldName=key, value=value)
        
    @classmethod
    def composite(cls, name, logic, conditions):
        return CompositeQuery(name=name, logic=logic, conditions=conditions)

    @classmethod
    def Not(cls, name, conditions):
        return cls.composite(name, QL.NOT, conditions)
        
    @classmethod
    def And(cls, name, conditions):
        return cls.composite(name, QL.AND, conditions)
        
    @classmethod
    def Or(cls, name, conditions):
        return cls.composite(name, QL.OR, conditions)
    