import { useRef, useState, useEffect } from "react";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import axios from '../api/axios';
import { Link } from "react-router-dom";

import Navbar from './Navbar';

const USER_REGEX = /^\S+@\S+\.\S+$/;
const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;
const REGISTER_URL = '/users';

  const Signup = () => {
    const userRef = useRef();
    const errRef = useRef();

    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);
    const [emailFocus, setEmailFocus] = useState(false);

    const [phone, setPhone] = useState('');
    // const [validPhone, setValidPhone] = useState(false);
    // const [phoneFocus, setPhoneFocus] = useState(false);

    const [pwd, setPwd] = useState('');
    const [validPwd, setValidPwd] = useState(false);
    const [pwdFocus, setPwdFocus] = useState(false);

    const [matchPwd, setMatchPwd] = useState('');
    const [validMatch, setValidMatch] = useState(false);
    const [matchFocus, setMatchFocus] = useState(false);

    const [errMsg, setErrMsg] = useState('');
    const [success, setSuccess] = useState(false);

    useEffect(() => {
      userRef.current.focus();
    }, []);

    useEffect(() => {
      setValidEmail(USER_REGEX.test(email));
    }, [email]);

    useEffect(() => {
      setValidPwd(PWD_REGEX.test(pwd));
      setValidMatch(pwd === matchPwd);
    }, [pwd, matchPwd]);

    useEffect(() => {
      setErrMsg('');
    }, [email, phone, pwd, matchPwd]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const isValidEntry = USER_REGEX.test(email) && PWD_REGEX.test(pwd);
    if (!isValidEntry) {
      setErrMsg("Invalid Entry");
      return;
    }

    try {
      const response = await axios.post(
        REGISTER_URL,
        JSON.stringify({ email, phone, pwd }),
        {
          headers: { 'Content-Type': 'application/json' },
          withCredentials: true
        }
      );
      console.log(JSON.stringify(response));
      console.log(JSON.stringify(response?.data));
      setSuccess(true);
      setEmail('');
      setPhone('');
      setPwd('');
      setMatchPwd('');
    } catch (err) {
      if (!err?.response) {
        setErrMsg('No Server Response');
      } else if (err.response?.status === 409) {
        setErrMsg('Phone Taken');
      } else {
        setErrMsg('Registration Failed')
      }
      errRef.current.focus();
    }
  };

  return (
    <>
      {success ? (
        <section>
          <h1>Success!</h1>
          <p>
            <Link to="#">Sign In</Link>
          </p>
        </section>
      ) : (
        <>
          <Navbar />
        <section className=" p-5">
          <div className="container">
            <div className="h1 p-5">
              <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
              <h1>Signup</h1>
            </div>
            <div className="align-items-center">
              <form className="align-items-center" onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">Email address:</label>
                  <input
                    type="email"
                    className="form-control w-50"
                    id="email"
                    name="email"
                    ref={userRef}
                    autoComplete="off"
                    onChange={(e) => setEmail(e.target.value)}
                    value={email}
                    aria-invalid={validEmail ? "false" : "true"}
                    aria-describedby="uidnote"
                    onFocus={() => setEmailFocus(true)}
                    onBlur={() => setEmailFocus(false)}
                  />
                  <p id="uidnote" className={emailFocus && email && !validEmail ? "instructions" : "offscreen"}>
                    <FontAwesomeIcon icon={faInfoCircle} />
                    4 to 24 characters.<br />
                    Must begin with a letter.<br />
                    Letters, numbers, underscores, hyphens allowed.
                  </p>
                  <div id="emailHelp" className="form-text">We'll never share your email with anyone else.</div>
                </div>
                <div className="mb-3">
                  <label htmlFor="phone" className="form-label">Phone:<span aria-label="required">*</span></label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    className="form-control w-50"
                    required
                    ref={userRef}
                    autoComplete="off"
                    onChange={(e) => setPhone(e.target.value)}
                    value={phone}
                    aria-describedby="uidnote"
                  />
                </div>
                <div className="form-group mb-3">
                  <fieldset>
                    <legend className="form-label small mb-3">Gender:</legend>
                    <div className="form-check">
                      <input className="form-check-input" type="radio" name="gender" id="female" value="female" />
                      <label className="form-check-label" htmlFor="female">Female</label>
                    </div>
                    <div className="form-check">
                      <input className="form-check-input" type="radio" name="gender" id="male" value="male" />
                      <label className="form-check-label" htmlFor="male">Male</label>
                    </div>
                    <div className="form-check">
                      <input className="form-check-input" type="radio" name="gender" id="none" value="none" />
                      <label className="form-check-label" htmlFor="none">Prefer Not to Say</label>
                    </div>
                  </fieldset>
                </div>
                <div className="mb-3">
                  <label htmlFor="InputPassword1" className="form-label">Password:<span aria-label="required">*</span></label>
                  <input
                    type="password"
                    className="form-control w-50"
                    id="InputPassword1"
                    name="password"
                    onChange={(e) => setPwd(e.target.value)}
                    value={pwd}
                    required
                    aria-invalid={validPwd ? "false" : "true"}
                    aria-describedby="pwdnote"
                    onFocus={() => setPwdFocus(true)}
                    onBlur={() => setPwdFocus(false)}
                  />
                  <p id="pwdnote" className={pwdFocus && !validPwd ? "instructions" : "offscreen"}>
                    <FontAwesomeIcon icon={faInfoCircle} />
                    8 to 24 characters.<br />
                    Must include uppercase and lowercase letters, a number and a special character.<br />
                    Allowed special characters: <span aria-label="exclamation mark">!</span> <span aria-label="at symbol">@</span> <span aria-label="hashtag">#</span> <span
                    aria-label="dollar sign">$</span> <span aria-label="percent">%</span>
                  </p>
                </div>
                <div className="mb-3">
                  <label htmlFor="confirm_pwd" className="form-label">Confirm Password:<span aria-label="required">*</span></label>
                  <input
                    type="password"
                    className="form-control w-50"
                    id="confirm_pwd"
                    onChange={(e) => setMatchPwd(e.target.value)}
                    value={matchPwd}
                    required
                    aria-invalid={validMatch ? "false" : "true"}
                    aria-describedby="confirmnote"
                    onFocus={() => setMatchFocus(true)}
                    onBlur={() => setMatchFocus(false)}
                  />
                  <p id="confirmnote" className={matchFocus && !validMatch ? "instructions" : "offscreen"}>
                    <FontAwesomeIcon icon={faInfoCircle} />
                    Must match the first password input field.
                  </p>
                  <div className="invalid-feedback" id="passwordMismatchError">Passwords must match.</div>
                </div>
                <button disabled={!validEmail || !validPwd || !validMatch ? true : false}>Sign Up</button>
              </form>
              <p>
                Already registered?<br />
                <span className="line">
                  <Link to="/">Sign In</Link>
                </span>
              </p>
            </div>
          </div>
        </section>
        </>
      )}
    </>
  );
}

export default Signup;
