from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql+psycopg2://postgres:7410@localhost/kpa_erp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Models

# Wheel Specification table
class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"
    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String)
    submittedBy = Column(String)
    submittedDate = Column(Date)
    status = Column(String)
    treadDiameterNew = Column(String)
    lastShopIssueSize = Column(String)
    condemningDia = Column(String)
    wheelGauge = Column(String)
    variationSameAxle = Column(String)
    variationSameBogie = Column(String)
    variationSameCoach = Column(String)
    wheelProfile = Column(String)
    intermediateWWP = Column(String)
    bearingSeatDiameter = Column(String)
    rollerBearingOuterDia = Column(String)
    rollerBearingBoreDia = Column(String)
    rollerBearingWidth = Column(String)
    axleBoxHousingBoreDia = Column(String)
    wheelDiscWidth = Column(String)

# Bogie Checksheet table
class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheets"
    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String)
    inspectionBy = Column(String)
    inspectionDate = Column(Date)
    status = Column(String)
    bogieNo = Column(String)
    makerYearBuilt = Column(String)
    incomingDivAndDate = Column(String)
    deficitComponents = Column(String)
    dateOfIOH = Column(String)
    bogieFrameCondition = Column(String)
    bolster = Column(String)
    bolsterSuspensionBracket = Column(String)
    lowerSpringSeat = Column(String)
    axleGuide = Column(String)
    cylinderBody = Column(String)
    pistonTrunnion = Column(String)
    adjustingTube = Column(String)
    plungerSpring = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# For Wheel Specification
class WheelSpecificationFields(BaseModel):
    treadDiameterNew: str
    lastShopIssueSize: str
    condemningDia: str
    wheelGauge: str
    variationSameAxle: str
    variationSameBogie: str
    variationSameCoach: str
    wheelProfile: str
    intermediateWWP: str
    bearingSeatDiameter: str
    rollerBearingOuterDia: str
    rollerBearingBoreDia: str
    rollerBearingWidth: str
    axleBoxHousingBoreDia: str
    wheelDiscWidth: str

class WheelSpecificationCreate(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: WheelSpecificationFields

class WheelSpecificationRead(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    status: str
    fields: WheelSpecificationFields

    class Config:
        from_attributes = True

# For Bogie Checksheet
class BogieDetails(BaseModel):
    bogieNo: str
    makerYearBuilt: str
    incomingDivAndDate: str
    deficitComponents: str
    dateOfIOH: str

class BogieChecks(BaseModel):
    bogieFrameCondition: str
    bolster: str
    bolsterSuspensionBracket: str
    lowerSpringSeat: str
    axleGuide: str

class BmbcChecks(BaseModel):
    cylinderBody: str
    pistonTrunnion: str
    adjustingTube: str
    plungerSpring: str

class BogieChecksheetCreate(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: date
    bogieDetails: BogieDetails
    bogieChecksheet: BogieChecks
    bmbcChecksheet: BmbcChecks

class BogieChecksheetRead(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: date
    status: str
    bogieDetails: BogieDetails
    bogieChecksheet: BogieChecks
    bmbcChecksheet: BmbcChecks

    class Config:
        orm_mode = True

#API responses
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: dict

class FilteredResponse(BaseModel):
    success: bool
    message: str
    data: List[dict]

#FastAPI app
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def record_exists(db, model, **kwargs):
    return db.query(model).filter_by(**kwargs).first() is not None

#Wheel Specification Routes
@app.post("/api/forms/wheel-specifications", response_model=SuccessResponse)
def create_wheel_spec(spec: WheelSpecificationCreate, db: Session = Depends(get_db)):
    # Check if already exists
    if record_exists(db, WheelSpecification, formNumber=spec.formNumber):
        raise HTTPException(status_code=400, detail="Form with this number already exists")
    # Create and save
    db_spec = WheelSpecification(
        formNumber=spec.formNumber,
        submittedBy=spec.submittedBy,
        submittedDate=spec.submittedDate,
        status="Saved",
        **spec.fields.dict()
    )
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return {
        "success": True,
        "message": "Wheel specification submitted successfully.",
        "data": {
            "formNumber": db_spec.formNumber,
            "submittedBy": db_spec.submittedBy,
            "submittedDate": db_spec.submittedDate,
            "status": db_spec.status
        }
    }

@app.get("/api/forms/wheel-specifications", response_model=FilteredResponse)
def get_wheel_specs(
    formNumber: Optional[str] = None,
    submittedBy: Optional[str] = None,
    submittedDate: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(WheelSpecification)
    if formNumber:
        query = query.filter(WheelSpecification.formNumber == formNumber)
    if submittedBy:
        query = query.filter(WheelSpecification.submittedBy == submittedBy)
    if submittedDate:
        query = query.filter(WheelSpecification.submittedDate == submittedDate)
    specs = query.all()
    data = [
        {
            "formNumber": spec.formNumber,
            "submittedBy": spec.submittedBy,
            "submittedDate": spec.submittedDate,
            "fields": {
                "treadDiameterNew": spec.treadDiameterNew,
                "lastShopIssueSize": spec.lastShopIssueSize,
                "condemningDia": spec.condemningDia,
                "wheelGauge": spec.wheelGauge,
                "variationSameAxle": spec.variationSameAxle,
                "variationSameBogie": spec.variationSameBogie,
                "variationSameCoach": spec.variationSameCoach,
                "wheelProfile": spec.wheelProfile,
                "intermediateWWP": spec.intermediateWWP,
                "bearingSeatDiameter": spec.bearingSeatDiameter,
                "rollerBearingOuterDia": spec.rollerBearingOuterDia,
                "rollerBearingBoreDia": spec.rollerBearingBoreDia,
                "rollerBearingWidth": spec.rollerBearingWidth,
                "axleBoxHousingBoreDia": spec.axleBoxHousingBoreDia,
                "wheelDiscWidth": spec.wheelDiscWidth
            }
        }
        for spec in specs
    ]
    return {
        "success": True,
        "message": "Filtered wheel specification forms fetched successfully.",
        "data": data
    }

#Bogie Checksheet Routes

@app.post("/api/forms/bogie-checksheet", response_model=SuccessResponse)
def create_bogie_checksheet(sheet: BogieChecksheetCreate, db: Session = Depends(get_db)):
    if record_exists(db, BogieChecksheet, formNumber=sheet.formNumber):
        raise HTTPException(status_code=400, detail="Form with this number already exists")
    db_sheet = BogieChecksheet(
        formNumber=sheet.formNumber,
        inspectionBy=sheet.inspectionBy,
        inspectionDate=sheet.inspectionDate,
        status="Saved",
        bogieNo=sheet.bogieDetails.bogieNo,
        makerYearBuilt=sheet.bogieDetails.makerYearBuilt,
        incomingDivAndDate=sheet.bogieDetails.incomingDivAndDate,
        deficitComponents=sheet.bogieDetails.deficitComponents,
        dateOfIOH=sheet.bogieDetails.dateOfIOH,
        bogieFrameCondition=sheet.bogieChecksheet.bogieFrameCondition,
        bolster=sheet.bogieChecksheet.bolster,
        bolsterSuspensionBracket=sheet.bogieChecksheet.bolsterSuspensionBracket,
        lowerSpringSeat=sheet.bogieChecksheet.lowerSpringSeat,
        axleGuide=sheet.bogieChecksheet.axleGuide,
        cylinderBody=sheet.bmbcChecksheet.cylinderBody,
        pistonTrunnion=sheet.bmbcChecksheet.pistonTrunnion,
        adjustingTube=sheet.bmbcChecksheet.adjustingTube,
        plungerSpring=sheet.bmbcChecksheet.plungerSpring
    )
    db.add(db_sheet)
    db.commit()
    db.refresh(db_sheet)
    return {
        "success": True,
        "message": "Bogie checksheet submitted successfully.",
        "data": {
            "formNumber": db_sheet.formNumber,
            "inspectionBy": db_sheet.inspectionBy,
            "inspectionDate": db_sheet.inspectionDate,
            "status": db_sheet.status
        }
    }

@app.get("/api/forms/bogie-checksheets", response_model=FilteredResponse)
def get_bogie_checksheets(
    formNumber: Optional[str] = None,
    inspectionBy: Optional[str] = None,
    inspectionDate: Optional[date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BogieChecksheet)
    if formNumber:
        query = query.filter(BogieChecksheet.formNumber == formNumber)
    if inspectionBy:
        query = query.filter(BogieChecksheet.inspectionBy == inspectionBy)
    if inspectionDate:
        query = query.filter(BogieChecksheet.inspectionDate == inspectionDate)
    sheets = query.all()
    data = [
        {
            "formNumber": sheet.formNumber,
            "inspectionBy": sheet.inspectionBy,
            "inspectionDate": sheet.inspectionDate,
            "bogieDetails": {
                "bogieNo": sheet.bogieNo,
                "makerYearBuilt": sheet.makerYearBuilt,
                "incomingDivAndDate": sheet.incomingDivAndDate,
                "deficitComponents": sheet.deficitComponents,
                "dateOfIOH": sheet.dateOfIOH
            },
            "bogieChecksheet": {
                "bogieFrameCondition": sheet.bogieFrameCondition,
                "bolster": sheet.bolster,
                "bolsterSuspensionBracket": sheet.bolsterSuspensionBracket,
                "lowerSpringSeat": sheet.lowerSpringSeat,
                "axleGuide": sheet.axleGuide
            },
            "bmbcChecksheet": {
                "cylinderBody": sheet.cylinderBody,
                "pistonTrunnion": sheet.pistonTrunnion,
                "adjustingTube": sheet.adjustingTube,
                "plungerSpring": sheet.plungerSpring
            }
        }
        for sheet in sheets
    ]
    return {
        "success": True,
        "message": "Filtered bogie checksheet forms fetched successfully.",
        "data": data
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
