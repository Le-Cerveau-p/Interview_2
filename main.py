from __future__ import annotations

import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request, g, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class AgentName(db.Model):
    __tablename__ = "agentname"

    name_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    pollingunit_uniqueid: Mapped[int] = mapped_column(Integer, nullable=False)


class AnnouncedLgaResult(db.Model):
    __tablename__ = "announced_lga_results"

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lga_name: Mapped[str] = mapped_column(String, nullable=False)
    party_abbreviation: Mapped[str] = mapped_column(String, nullable=False)
    party_score: Mapped[int] = mapped_column(Integer, nullable=False)
    entered_by_user: Mapped[str] = mapped_column(String, nullable=False)
    date_entered: Mapped[str] = mapped_column(String, nullable=False)
    user_ip_address: Mapped[str] = mapped_column(String, nullable=False)


class AnnouncedPuResult(db.Model):
    __tablename__ = "announced_pu_results"

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    polling_unit_uniqueid: Mapped[str] = mapped_column(String, nullable=False)
    party_abbreviation: Mapped[str] = mapped_column(String, nullable=False)
    party_score: Mapped[int] = mapped_column(Integer, nullable=False)
    entered_by_user: Mapped[str] = mapped_column(String, nullable=False)
    date_entered: Mapped[str] = mapped_column(String, nullable=False)
    user_ip_address: Mapped[str] = mapped_column(String, nullable=False)


class AnnouncedStateResult(db.Model):
    __tablename__ = "announced_state_results"

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    state_name: Mapped[str] = mapped_column(String, nullable=False)
    party_abbreviation: Mapped[str] = mapped_column(String, nullable=False)
    party_score: Mapped[int] = mapped_column(Integer, nullable=False)
    entered_by_user: Mapped[str] = mapped_column(String, nullable=False)
    date_entered: Mapped[str] = mapped_column(String, nullable=False)
    user_ip_address: Mapped[str] = mapped_column(String, nullable=False)


class AnnouncedWardResult(db.Model):
    __tablename__ = "announced_ward_results"

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ward_name: Mapped[str] = mapped_column(String, nullable=False)
    party_abbreviation: Mapped[str] = mapped_column(String, nullable=False)
    party_score: Mapped[int] = mapped_column(Integer, nullable=False)
    entered_by_user: Mapped[str] = mapped_column(String, nullable=False)
    date_entered: Mapped[str] = mapped_column(String, nullable=False)
    user_ip_address: Mapped[str] = mapped_column(String, nullable=False)


class LGA(db.Model):
    __tablename__ = "lga"

    uniqueid: Mapped[int] = mapped_column(Integer, primary_key=True)
    lga_id: Mapped[int] = mapped_column(Integer, unique=True)
    lga_name: Mapped[str] = mapped_column(String, nullable=False)
    state_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lga_description: Mapped[str] = mapped_column(String, nullable=True)
    entered_by_user: Mapped[str] = mapped_column(String, nullable=False)
    date_entered: Mapped[str] = mapped_column(String, nullable=False)
    user_ip_address: Mapped[str] = mapped_column(String, nullable=False)


class Party(db.Model):
    __tablename__ = "party"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    partyid: Mapped[str] = mapped_column(String, nullable=False)
    partyname: Mapped[str] = mapped_column(String, nullable=False)


class PollingUnit(db.Model):
    __tablename__ = "polling_unit"

    uniqueid: Mapped[int] = mapped_column(Integer, primary_key=True)
    polling_unit_id: Mapped[int] = mapped_column(Integer, unique=True)
    ward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    lga_id: Mapped[int] = mapped_column(Integer, nullable=False)
    uniquewardid: Mapped[int] = mapped_column(Integer, nullable=True)
    polling_unit_number: Mapped[str] = mapped_column(String, nullable=True)
    polling_unit_name: Mapped[str] = mapped_column(String, nullable=True)
    polling_unit_description: Mapped[str] = mapped_column(String, nullable=True)
    lat: Mapped[str] = mapped_column(String, nullable=True)
    long: Mapped[str] = mapped_column(String, nullable=True)
    entered_by_user: Mapped[str] = mapped_column(String, nullable=True)
    date_entered: Mapped[str] = mapped_column(String, nullable=True)
    user_ip_address: Mapped[str] = mapped_column(String, nullable=True)


class State(db.Model):
    __tablename__ = "states"

    state_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    state_name: Mapped[str] = mapped_column(String(50), nullable=False)


class Ward(db.Model):
    __tablename__ = "ward"

    uniqueid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ward_name: Mapped[str] = mapped_column(String(50), nullable=False)
    lga_id: Mapped[int] = mapped_column(Integer, nullable=False)
    ward_description: Mapped[str] = mapped_column(String, nullable=True)
    entered_by_user: Mapped[str] = mapped_column(String(50), nullable=False)
    date_entered: Mapped[str] = mapped_column(String, nullable=False)
    user_ip_address: Mapped[str] = mapped_column(String(50), nullable=False)





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/q1")
def q1():
    announced_pu = db.session.execute(db.select(AnnouncedPuResult)).scalars().all()
    available_pu = []
    for record in announced_pu:
        if int(record.polling_unit_uniqueid) not in available_pu:
            available_pu.append(int(record.polling_unit_uniqueid))
    available_pu.sort()
    print(available_pu)
    total_poll_rec = []
    for pu in available_pu:
        poll_unit = db.one_or_404(db.select(PollingUnit).filter_by(uniqueid=str(pu)))
        poll_unit_record = []
        for record in announced_pu:
            if record.polling_unit_uniqueid == str(pu):
                new_info = {"pu_num": poll_unit.polling_unit_number,
                            "pu_name": poll_unit.polling_unit_name,
                            "party": record.party_abbreviation,
                            "score":record.party_score,
                            "time":record.date_entered}
                poll_unit_record.append(new_info)
        total_poll_rec.append(poll_unit_record)
    print(total_poll_rec)
    return render_template("q1.html", total_poll_rec=total_poll_rec)


@app.route("/q2", methods=["GET", "POST"])
def q2():
    lgas = db.session.execute(db.select(LGA)).scalars().all()
    LGAs = [lga.lga_name for lga in lgas]
    if request.method == "POST":
        if request.form['LGA'] != 'Select LGA':
            parties = db.session.execute(db.select(Party)).scalars().all()
            aval_parties = [party.partyid for party in parties]
            party_total = {party:0 for party in aval_parties}
            lga_selected = request.form['LGA']
            lga_selected_id = db.one_or_404(db.select(LGA).filter_by(lga_name=lga_selected)).lga_id
            p_lga_recs = db.session.execute(db.select(PollingUnit).filter_by(lga_id=lga_selected_id)).scalars().all()
            for p_lga_rec in p_lga_recs:
                # print(p_lga_rec.polling_unit_name)
                pol_recs = db.session.execute(db.select(AnnouncedPuResult).filter_by(polling_unit_uniqueid=p_lga_rec.uniqueid)).scalars().all()
                for pol_rec in pol_recs:
                    for party in aval_parties:
                        if pol_rec.party_abbreviation == party:
                            party_total[party] += pol_rec.party_score
            party_total_list = [{"party_name":key, "score": party_total[key]} for key in party_total]

            return render_template("q2.html", LGAs=LGAs, party_total_list=party_total_list, id=lga_selected_id, lga=lga_selected)
        else:
            return render_template("q2.html", LGAs=LGAs, null_pick=True)
    return render_template("q2.html", LGAs=LGAs)


@app.route("/q3", methods=["GET", "POST"])
def q3():
    if request.method == "POST":

        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        new_record = AnnouncedPuResult(
        polling_unit_uniqueid=request.form['polling_unit_uniqueid'],
        party_abbreviation=request.form['party_abbreviation'],
        party_score=request.form['party_score'],
        entered_by_user=request.form['entered_by_user'],
        date_entered=formatted_date,
        user_ip_address=request.remote_addr
        )
        db.session.add(new_record)
        db.session.commit()
        return render_template('q3.html', msg=True)
    return render_template("q3.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)